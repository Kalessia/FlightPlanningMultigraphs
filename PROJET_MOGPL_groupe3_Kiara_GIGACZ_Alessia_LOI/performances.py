from multigraph import Multigraph
from minimalDistanceProblem import MinimalDistanceProblem

import time
import datetime

import random
import scipy.stats as st
import numpy as np

import matplotlib.pyplot as plt

verbose = False




def randomMultigraphe(n, m, interval_dates, verbose=False):
	"""
	"""
	if n == 0 or m < n:
		return None

	vertices = ["s"+str(i) for i in range(n)]
	edges = []

	arcsADistribuer = m-n
	tabNbSuccesseurs = [1] * n

	z = random.randint(1, int(np.log(n)) + 1) # nombre de feuilles (sommets finaux sans successeurs) souhaitées ; fonction logarithme népérien
	l = random.randint(1, int((n % m)) + 1) # lambda

	# Parametrage de truncnorm( (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd )
	borneInf = interval_dates[0] # low
	borneSup = interval_dates[1] # upp
	ecartType = int(interval_dates[1]/5) # sd
	# la moyenne mean vaut l'index du sommet en cours de traitement

	# Choix du nombre de successeurs pour chaque sommet s(i) dans la limite de m totales
	while arcsADistribuer > 0:
		i = random.randint(0,n-1)
		tabNbSuccesseurs[i] += 1
		arcsADistribuer -= 1


	for i in range(len(tabNbSuccesseurs)-1):
		edges.append((vertices[i], vertices[i+1], borneInf, l))
		p = random.uniform(0,1)

		# Probabilité de l'attribuire aux premieres cases
		if (p < 0.2) :
			source = vertices[0] # racine
			for j in range(1, tabNbSuccesseurs[i]):
				dest = random.choice(vertices[1:z+2]) # choix parmi les premiers z sommets sauf la racine
				date = st.truncnorm.rvs( (borneInf - int(source[1])) / ecartType, (borneSup - int(source[1])) / ecartType, loc=int(source[1]), scale=ecartType )
				edges.append((source, dest, int(date), l))
		
		elif (p > 0.8) : # Probabilité de l'attribuire aux dernieres cases
			source = random.choice(vertices[:-(z+2)]) # choix parmi les z*3 derniers sommets
			for j in range(1, tabNbSuccesseurs[i]):
				dest = random.choice(vertices[vertices.index(source)+1:])
				date = st.truncnorm.rvs( (borneInf - int(source[1])) / ecartType, (borneSup - int(source[1])) / ecartType, loc=int(source[1]), scale=ecartType )
				edges.append((source, dest, int(date), l))
		
		else:
			nbS = tabNbSuccesseurs[i]
			if ((i+nbS-1) < n):
				k = i	
			else:
				k = n-(nbS+1)

			source = vertices[k]
			for j in range(1, nbS):
				dest = vertices[k+j]
				date = st.truncnorm.rvs( (borneInf - int(source[1])) / ecartType, (borneSup - int(source[1])) / ecartType, loc=int(source[1]), scale=ecartType )
				edges.append((source, dest, int(date), l))
	
	for j in range(tabNbSuccesseurs[n-1]):
		edges.append((vertices[n-random.randint(2,n)], vertices[n-1], borneInf, l))

		
	if len(vertices) != n or len(edges) != m :
		return None
			
	return Multigraph(n, m, vertices, edges)






# Méthode permettant d'afficher un graphique de comparaison des performances ("temps de calcul" et "qualité des Solutions") de l'algorithme choisi
def plotPerformances_n(minN, maxN, m_fixe, interval_dates_fixe, nbTests, nbIterations, verbose=False, save = False):
	ordonnee_tGlobal = []  # liste des temps de calcul moyen, vue globale sur le programme
	ordonnee_tInit = []  # liste des temps de calcul moyen, vue sur l'initialisation (transformation en graphe + calcul d'arbre couvrant)
	ordonnee_tType1 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type1
	ordonnee_tType2 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type2
	ordonnee_tType3 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type3
	ordonnee_tType4 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type4
	ordonnee_tType4_LP = []  # liste des temps de calcul moyen, vue sur l'algorithme de type4_LP

	abscisse_n = []
	

	for nb in range(1, nbTests+1):
		n = int(minN + (maxN-minN/nbTests*nb))
		
		x = "s0"
		y = "s" + str(n-1)

		abscisse_n.append(n)

		# Méthode permettant de générer des graphes aléatoires
		init_tStart = time.time() # init = initialisation programme = transformation en graphe + calcul d'arbre couvrant
		mg = randomMultigraphe(n, m_fixe, interval_dates_fixe)
		g = mg.transform_to_graph()
		p = MinimalDistanceProblem(g, x, y, interval_dates_fixe)
		init_tEnd = time.time()
		ordonnee_tInit.append(init_tEnd - init_tStart)

		tGlobal = []
		tInit = []
		tType1 = []
		tType2 = []
		tType3 = []
		tType4 = []
		tType4_LP = []

		for ite in range(nbIterations):

			global_tStart = time.time() # global = temps d'execution du programme entier = initialisation + calcul chemins
			
			type1_tStart = time.time()
			p.earliest_arrival()
			type1_tEnd = time.time()

			type2_tStart = time.time()
			p.latest_departure()
			type2_tEnd = time.time()

			type3_tStart = time.time()
			p.fastest()
			type3_tEnd = time.time()

			type4_tStart = time.time()
			p.shortest()
			type4_tEnd = time.time()

			global_tEnd = time.time()

			type4_LP_tStart = time.time()
			p.shortest_LP()
			type4_LP_tEnd = time.time()


			tGlobal.append(global_tEnd - global_tStart)
			tInit.append(init_tEnd - init_tStart)
			tType1.append(type1_tEnd - type1_tStart)
			tType2.append(type2_tEnd - type2_tStart)
			tType3.append(type3_tEnd - type3_tStart)
			tType4.append(type4_tEnd - type4_tStart)
			tType4_LP.append(type4_LP_tEnd - type4_LP_tStart)

			if verbose:
				print("Temps d'executions rélatifs à l'itération n.", ite, "\n\ttGlobal :", tGlobal, "\n\ttInit :", tInit, "\n\ttType1 :", tType1, "\n\ttType2 :", tType2, "\n\ttType3 :", tType3, "\n\ttType4 :", tType4)

		ordonnee_tGlobal.append( (sum(tGlobal)/len(tGlobal)) )
		ordonnee_tType1.append( (sum(tType1)/len(tType1)) )
		ordonnee_tType2.append( (sum(tType2)/len(tType2)) )
		ordonnee_tType3.append( (sum(tType3)/len(tType3)) )
		ordonnee_tType4.append( (sum(tType4)/len(tType4)) )
		ordonnee_tType4_LP.append( (sum(tType4_LP)/len(tType4_LP)) )


	if verbose:
		print("Temps d'executions moyens rélatifs au test n.", nb, "\n\tordonnee_tGlobal :", ordonnee_tGlobal, "\n\tordonnee_tInit :", ordonnee_tInit, "\n\tordonnee_tType1 :", ordonnee_tType1, "\n\tordonnee_tType2 :", ordonnee_tType2, "\n\tordonnee_tType3 :", ordonnee_tType3, "\n\tordonnee_tType4 :", ordonnee_tType4)
	
	
	#Affichage graphique
	plt.figure()
	plt.suptitle("Performances", size = 20, color = 'red')
	plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
	plt.grid(True)

	# Construction et affichage du tracé "temps de calcul"
	plt.tight_layout()
	plt.title("Analyse du temps de calcul en fonction du nombre de sommets n")
	plt.xlabel("n") # nombre de sommets du graphe G
	plt.ylabel("t(n)") # temps de calcul en fonction du nombre de sommets du graphe G
	plt.plot(abscisse_n, ordonnee_tGlobal, label = "temps Global")
	plt.plot(abscisse_n, ordonnee_tInit, label = "temps initialisation")
	plt.plot(abscisse_n, ordonnee_tType1, label = "type I : chemin d'arrivée au plus tôt")
	plt.plot(abscisse_n, ordonnee_tType2, label = "type II : chemin de départ au plus tard")
	plt.plot(abscisse_n, ordonnee_tType3, label = "type III : chemin le plus rapide")
	plt.plot(abscisse_n, ordonnee_tType4, label = "type VI : plus court chemin")
	plt.legend()
	
	# Sauvegarde du tracé
	if (save):
		plt.savefig("TestsResults/TestResults_n/" + str(datetime.date.today()) + str(datetime.datetime.now().strftime("_%H_%M_%S")) + ".jpeg", transparent = True)
	
	plt.show()

	#Affichage graphique
	plt.figure()
	plt.suptitle("Performances", size = 20, color = 'red')
	plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
	plt.grid(True)

	# Construction et affichage du tracé "temps de calcul"
	plt.tight_layout()
	plt.title("Analyse du temps de calcul en fonction du nombre de sommets n")
	plt.xlabel("n") # nombre de sommets du graphe G
	plt.ylabel("t(n)") # temps de calcul en fonction du nombre de sommets du graphe G
	plt.plot(abscisse_n, ordonnee_tType4, label = "type VI : plus court chemin")
	plt.plot(abscisse_n, ordonnee_tType4_LP, label = "type VI LP : LP plus court chemin")
	plt.legend()
	
	# Sauvegarde du tracé
	if (save):
		plt.savefig("TestsResults/TestResults_n/" + str(datetime.date.today()) + str(datetime.datetime.now().strftime("_%H_%M_%S")) + ".jpeg", transparent = True)
	
	plt.show()




# Méthode permettant d'afficher un graphique de comparaison des performances ("temps de calcul" et "qualité des Solutions") de l'algorithme choisi
def plotPerformances_m(n_fixe, minM, maxM, interval_dates_fixe, nbTests, nbIterations, verbose=False, save = False):
	ordonnee_tGlobal = []  # liste des temps de calcul moyen, vue globale sur le programme
	ordonnee_tInit = []  # liste des temps de calcul moyen, vue sur l'initialisation (transformation en graphe + calcul d'arbre couvrant)
	ordonnee_tType1 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type1
	ordonnee_tType2 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type2
	ordonnee_tType3 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type3
	ordonnee_tType4 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type4
	ordonnee_tType4_LP = []  # liste des temps de calcul moyen, vue sur l'algorithme de type4_LP
	

	abscisse_m = []
	

	for nb in range(1, nbTests+1):
		m = int(minM + (maxM-minM/nbTests*nb))
		
		x = "s0"
		y = "s" + str(n_fixe-1)

		abscisse_m.append(m)

		# Méthode permettant de générer des graphes aléatoires
		init_tStart = time.time() # init = initialisation programme = transformation en graphe + calcul d'arbre couvrant
		mg = randomMultigraphe(n_fixe, m, interval_dates_fixe)
		g = mg.transform_to_graph()
		p = MinimalDistanceProblem(g, x, y, interval_dates_fixe)
		init_tEnd = time.time()
		ordonnee_tInit.append(init_tEnd - init_tStart)

		tGlobal = []
		tInit = []
		tType1 = []
		tType2 = []
		tType3 = []
		tType4 = []
		tType4_LP = []


		for ite in range(nbIterations):

			global_tStart = time.time() # global = temps d'execution du programme entier = initialisation + calcul chemins
			
			type1_tStart = time.time()
			p.earliest_arrival()
			type1_tEnd = time.time()

			type2_tStart = time.time()
			p.latest_departure()
			type2_tEnd = time.time()

			type3_tStart = time.time()
			p.fastest()
			type3_tEnd = time.time()

			type4_tStart = time.time()
			p.shortest()
			type4_tEnd = time.time()

			global_tEnd = time.time()

			type4_LP_tStart = time.time()
			p.shortest_LP()
			type4_LP_tEnd = time.time()


			tGlobal.append(global_tEnd - global_tStart)
			tInit.append(init_tEnd - init_tStart)
			tType1.append(type1_tEnd - type1_tStart)
			tType2.append(type2_tEnd - type2_tStart)
			tType3.append(type3_tEnd - type3_tStart)
			tType4.append(type4_tEnd - type4_tStart)
			tType4_LP.append(type4_LP_tEnd - type4_LP_tStart)

			if verbose:
				print("Temps d'executions rélatifs à l'itération n.", ite, "\n\ttGlobal :", tGlobal, "\n\ttInit :", tInit, "\n\ttType1 :", tType1, "\n\ttType2 :", tType2, "\n\ttType3 :", tType3, "\n\ttType4 :", tType4)

		ordonnee_tGlobal.append( (sum(tGlobal)/len(tGlobal)) )
		ordonnee_tType1.append( (sum(tType1)/len(tType1)) )
		ordonnee_tType2.append( (sum(tType2)/len(tType2)) )
		ordonnee_tType3.append( (sum(tType3)/len(tType3)) )
		ordonnee_tType4.append( (sum(tType4)/len(tType4)) )
		ordonnee_tType4_LP.append( (sum(tType4_LP)/len(tType4_LP)) )


	if verbose:
		print("Temps d'executions moyens rélatifs au test n.", nb, "\n\tordonnee_tGlobal :", ordonnee_tGlobal, "\n\tordonnee_tInit :", ordonnee_tInit, "\n\tordonnee_tType1 :", ordonnee_tType1, "\n\tordonnee_tType2 :", ordonnee_tType2, "\n\tordonnee_tType3 :", ordonnee_tType3, "\n\tordonnee_tType4 :", ordonnee_tType4)
	
	
	#Affichage graphique
	plt.figure()
	plt.suptitle("Performances", size = 20, color = 'red')
	plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
	plt.grid(True)

	plt.title("Analyse du temps de calcul en fonction du nombre d'arcs m")
	plt.xlabel("m") # nombre d'arcs du graphe G
	plt.ylabel("t(m)") # temps de calcul en fonction du nombre d'arcs du graphe G
	plt.plot(abscisse_m, ordonnee_tGlobal, label = "temps Global")
	plt.plot(abscisse_m, ordonnee_tInit, label = "temps initialisation")
	plt.plot(abscisse_m, ordonnee_tType1, label = "type I : chemin d'arrivée au plus tôt")
	plt.plot(abscisse_m, ordonnee_tType2, label = "type II : chemin de départ au plus tard")
	plt.plot(abscisse_m, ordonnee_tType3, label = "type III : chemin le plus rapide")
	plt.plot(abscisse_m, ordonnee_tType4, label = "type VI : plus court chemin")

	# Sauvegarde du tracé
	if (save):
		plt.savefig("TestsResults/TestsResults/m/" + str(datetime.date.today()) + str(datetime.datetime.now().strftime("_%H_%M_%S")) + ".jpeg", transparent = True)
	
	plt.show()



	#Affichage graphique
	plt.figure()
	plt.suptitle("Performances", size = 20, color = 'red')
	plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
	plt.grid(True)

	plt.title("Analyse du temps de calcul en fonction du nombre d'arcs m")
	plt.xlabel("m") # nombre d'arcs du graphe G
	plt.ylabel("t(m)") # temps de calcul en fonction du nombre d'arcs du graphe G
	plt.plot(abscisse_m, ordonnee_tType4, label = "type VI : plus court chemin")
	plt.plot(abscisse_m, ordonnee_tType4_LP, label = "type VI LP : LP plus court chemin")


	# Sauvegarde du tracé
	if (save):
		plt.savefig("TestsResults/TestsResults/m/" + str(datetime.date.today()) + str(datetime.datetime.now().strftime("_%H_%M_%S")) + ".jpeg", transparent = True)
	
	plt.show()


# Méthode permettant d'afficher un graphique de comparaison des performances ("temps de calcul" et "qualité des Solutions") de l'algorithme choisi
def plotPerformances_d(n_fixe, m_fixe, maxInterval_dates, nbTests, nbIterations, verbose=False, save = False):
	ordonnee_tGlobal = []  # liste des temps de calcul moyen, vue globale sur le programme
	ordonnee_tInit = []  # liste des temps de calcul moyen, vue sur l'initialisation (transformation en graphe + calcul d'arbre couvrant)
	ordonnee_tType1 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type1
	ordonnee_tType2 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type2
	ordonnee_tType3 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type3
	ordonnee_tType4 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type4
	ordonnee_tType4_LP = []  # liste des temps de calcul moyen, vue sur l'algorithme de type4_LP

	abscisse_d = []
	

	for nb in range(1, nbTests+1):
		interval_dates = [ int(maxInterval_dates[0]/nbTests*nb), int(maxInterval_dates[1]/nbTests*nb) ]
		
		x = "s0"
		y = "s" + str(n_fixe-1)


		abscisse_d.append("[" + str(maxInterval_dates[0]/nbTests*nb) + "," + str(maxInterval_dates[1]/nbTests*nb) + "]")

		# Méthode permettant de générer des graphes aléatoires
		init_tStart = time.time() # init = initialisation programme = transformation en graphe + calcul d'arbre couvrant
		mg = randomMultigraphe(n_fixe, m_fixe, interval_dates)
		g = mg.transform_to_graph()
		p = MinimalDistanceProblem(g, x, y, interval_dates)
		init_tEnd = time.time()
		ordonnee_tInit.append(init_tEnd - init_tStart)

		tGlobal = []
		tInit = []
		tType1 = []
		tType2 = []
		tType3 = []
		tType4 = []
		tType4_LP = []


		for ite in range(nbIterations):

			global_tStart = time.time() # global = temps d'execution du programme entier = initialisation + calcul chemins
			
			type1_tStart = time.time()
			p.earliest_arrival()
			type1_tEnd = time.time()

			type2_tStart = time.time()
			p.latest_departure()
			type2_tEnd = time.time()

			type3_tStart = time.time()
			p.fastest()
			type3_tEnd = time.time()

			type4_tStart = time.time()
			p.shortest()
			type4_tEnd = time.time()

			global_tEnd = time.time()

			type4_LP_tStart = time.time()
			p.shortest_LP()
			type4_LP_tEnd = time.time()


			tGlobal.append(global_tEnd - global_tStart)
			tInit.append(init_tEnd - init_tStart)
			tType1.append(type1_tEnd - type1_tStart)
			tType2.append(type2_tEnd - type2_tStart)
			tType3.append(type3_tEnd - type3_tStart)
			tType4.append(type4_tEnd - type4_tStart)
			tType4_LP.append(type4_LP_tEnd - type4_LP_tStart)


			if verbose:
				print("Temps d'executions rélatifs à l'itération n.", ite, "\n\ttGlobal :", tGlobal, "\n\ttInit :", tInit, "\n\ttType1 :", tType1, "\n\ttType2 :", tType2, "\n\ttType3 :", tType3, "\n\ttType4 :", tType4)

		ordonnee_tGlobal.append( (sum(tGlobal)/len(tGlobal)) )
		ordonnee_tType1.append( (sum(tType1)/len(tType1)) )
		ordonnee_tType2.append( (sum(tType2)/len(tType2)) )
		ordonnee_tType3.append( (sum(tType3)/len(tType3)) )
		ordonnee_tType4.append( (sum(tType4)/len(tType4)) )
		ordonnee_tType4_LP.append( (sum(tType4_LP)/len(tType4_LP)) )


	if verbose:
		print("Temps d'executions moyens rélatifs au test n.", nb, "\n\tordonnee_tGlobal :", ordonnee_tGlobal, "\n\tordonnee_tInit :", ordonnee_tInit, "\n\tordonnee_tType1 :", ordonnee_tType1, "\n\tordonnee_tType2 :", ordonnee_tType2, "\n\tordonnee_tType3 :", ordonnee_tType3, "\n\tordonnee_tType4 :", ordonnee_tType4)
	
	
	#Affichage graphique
	plt.figure()
	plt.suptitle("Performances", size = 20, color = 'red')
	plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
	plt.grid(True)

	plt.title("Analyse du temps de calcul en fonction de l'intervalle de dates choisies interval_dates")
	plt.xlabel("interval_dates") # nombre de sommets du graphe G
	plt.ylabel("t(interval_dates)") # temps de calcul en fonction de l'interval de dates choisies du graphe G
	plt.plot(abscisse_d, ordonnee_tGlobal, label = "temps Global")
	plt.plot(abscisse_d, ordonnee_tInit, label = "temps initialisation")
	plt.plot(abscisse_d, ordonnee_tType1, label = "type I : chemin d'arrivée au plus tôt")
	plt.plot(abscisse_d, ordonnee_tType2, label = "type II : chemin de départ au plus tard")
	plt.plot(abscisse_d, ordonnee_tType3, label = "type III : chemin le plus rapide")
	plt.plot(abscisse_d, ordonnee_tType4, label = "type VI : plus court chemin")

	# Sauvegarde du tracé
	if (save):
		plt.savefig("TestsResults/TestResults_interval_dates/" + str(datetime.date.today()) + str(datetime.datetime.now().strftime("_%H_%M_%S")) + ".jpeg", transparent = True)
	
	plt.show()


	#Affichage graphique
	plt.figure()
	plt.suptitle("Performances", size = 20, color = 'red')
	plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
	plt.grid(True)

	plt.title("Analyse du temps de calcul en fonction de l'intervalle de dates choisies interval_dates")
	plt.xlabel("interval_dates") # nombre de sommets du graphe G
	plt.ylabel("t(interval_dates)") # temps de calcul en fonction de l'interval de dates choisies du graphe G
	plt.plot(abscisse_d, ordonnee_tType4, label = "type VI : plus court chemin")
	plt.plot(abscisse_d, ordonnee_tType4_LP, label = "type VI LP : plus court chemin")

	# Sauvegarde du tracé
	if (save):
		plt.savefig("TestsResults/TestResults_interval_dates/" + str(datetime.date.today()) + str(datetime.datetime.now().strftime("_%H_%M_%S")) + ".jpeg", transparent = True)
	
	plt.show()







def performances():
	
	nbTests = 2
	nbIterations = 1
	verbose=False
	save = False

	# Paramètres choisis pour les tests, gérés dans plotPerformances pour la création des random multigraphes:
	# 	x = sommet initial s0
	# 	y = dernier sommet s(n-1)
	# 	interval = interval_fixe ou maxInterval_dates

	# Parametres pour plotPerformances_n
	minN = 10
	maxN = 30
	
	# Parametres pour plotPerformances_m
	minM = 30
	maxM = 90
	
	# Parametres pour plotPerformances_d
	maxInterval_dates = [1,30]

	n_fixe = 10
	m_fixe = 100
	interval_dates_fixe = [1,10]


	plotPerformances_n(minN, maxN, m_fixe, interval_dates_fixe, nbTests, nbIterations, verbose, save)
	plotPerformances_m(n_fixe, minM, maxM, interval_dates_fixe, nbTests, nbIterations, verbose, save)
	plotPerformances_d(n_fixe, m_fixe, maxInterval_dates, nbTests, nbIterations, verbose, save)

performances()