from multigraph import Multigraph
from graph import Graph
from minimalDistanceProblem import MinimalDistanceProblem

import time
import datetime

from math import floor, ceil 
import random
import scipy.stats as st
import numpy as np

import matplotlib.pyplot as plt

verbose = False




def randomMultigraphe(n, m, interval_dates):
	"""
	"""
	if n == 0 or m < n:
		return None

	vertices = ["s"+str(i) for i in range(n)]
	
	arcsADistribuer = m
	edges = []
	z = random.randint(1, int(np.log(n)) + 1) # nombre de feuilles (sommets finaux sans successeurs) souhaitées ; fonction logarithme népérien
	l = random.randint(1, int((n % m)) + 1) # lambda
	k = z*3 + 1 # nombre de arcs supplementaires que on réserve pour les sommets racine et feuilles

	# Parametrisation de truncnorm( (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd )
	borneInf = interval_dates[0] # low
	borneSup = interval_dates[1] # upp
	ecartType = int(interval_dates[1]/5) # sd
	# la moyenne mean vaut l'index du sommet en cours de traitement

	for i in range(m):

		if arcsADistribuer < 1:
			break

		# On attribue les premieres n-1 arcs pour rélier tous les sommets, tel que tout sommet est rélié à au moins un autre sommet
		if (i < n):
			print("on rentre car i =", i)
			source = vertices[i]
			nbSuccesseursSource = random.randint(1, int(((n % m))/2) + 1)
			if ( (i + nbSuccesseursSource) > n ):
				print("en effet:", i + nbSuccesseursSource, ">", n, "donc", n - i - 1 )
				nbSuccesseursSource = n - i - 1
			for j in range(1, nbSuccesseursSource):
				dest = vertices[i+j]
				#date = st.skewnorm.rvs(3, i, 5)
				#date = int(st.truncnorm.rvs( (borneInf - int(source[1])) / ecartType, (borneSup - int(source[1])) / ecartType, loc=int(source[1]), scale=ecartType ) )
				date = random.randint(borneInf, borneSup + 1)
				edges.append((source, dest, date, l))	# format arc : (source : str, dest : str, date : int, lambda l : int)
				arcsADistribuer -= 1
				print(i, "apres 1 :", arcsADistribuer)
				if arcsADistribuer == 0:
					break
				

		# On s'assure de réserver les derniers arcs à distribuer pour les sommets racine et feuilles
		elif (arcsADistribuer < k):
			print("k =", k)
			x = arcsADistribuer # <--------------------------- ne surtout pas effacer ce passage XD
			for j in range(floor(x/2)): # floor : partie entière inférieure
				print("test arcsADistribuer", arcsADistribuer)
				print("test repartition", floor(arcsADistribuer/2), ceil(arcsADistribuer/2))
				source = vertices[0] # racine
				dest = random.choice(vertices[1:z+2]) # choix parmi les premiers z sommets sauf la racine
				print("ja", j)
				#date = st.skewnorm.rvs(3, i, 5)
				#date = int( st.truncnorm.rvs( (borneInf - int(source[1])) / ecartType, (borneSup - int(source[1])) / ecartType, loc=int(source[1]), scale=ecartType ) )
				date = random.randint(borneInf, borneSup + 1)
				edges.append((source, dest, date, l))
				arcsADistribuer -= 1
				print(i, "apres 2a :", arcsADistribuer)

			for j in range(ceil(x/2)): # floor : partie entière superièure
				print("sono dentro b, j vale", j)
				print("sono dentro b, ceil", ceil(arcsADistribuer/2))
				source = random.choice(vertices[:-z*3+1]) # choix parmi les z*3 derniers sommets
				dest = random.choice(vertices[vertices.index(source)+1:])
				print("jb", j)
				#date = st.skewnorm.rvs(3, i, 5)
				#date = int( st.truncnorm.rvs( (borneInf - int(source[1])) / ecartType, (borneSup - int(source[1])) / ecartType, loc=int(source[1]), scale=ecartType ) )
				date = random.randint(borneInf, borneSup + 1)
				edges.append((source, dest, date, l))
				arcsADistribuer -= 1
				print(i, "apres 2b :", arcsADistribuer)

			break

		# Si les 2 cas précedents sont réspectés, le reste des arcs est distribué aléatoirement
		else:
			source = random.choice(vertices[:-z]) # tous les valeurs sauf le derniers z sommets (feuilles)
			dest = random.choice(vertices[vertices.index(source)+1:]) # tous les valeurs sauf le premier sommet (racine)
			#date = st.skewnorm.rvs(3, i, 5)
			#date = int( st.truncnorm.rvs(borneInf - int(source[1])) / ecartType, (borneSup - int(source[1])) / ecartType, loc=int(source[1]), scale=ecartType )
			date = random.randint(borneInf, borneSup + 1)
			edges.append((source, dest, date, l))	# format arc : (source : str, dest : str, date : int, lambda l : int)
			arcsADistribuer -= 1
			print(i, "apres 3 :", arcsADistribuer)


	print("len(vertices :", len(vertices), ", n :", n, ", len(edges) :", len(edges), ", m :", m)

	if len(vertices) != n or len(edges) != m :
		return None

	# Si i<n, alors il y a probablement des sommets non réliés par des arcs au multigraphe.
	# On rajoute la quantité minimale d'arcs à partir de ces sommets vers des successeurs pour ne pas faire planter la simulation.
	if (i < n) :
		print("on a i <n car i = ", i)
		nbSuccesseursSource = n-i
		for j in range(nbSuccesseursSource):
			source = vertices[i-1]
			dest = random.choice(vertices[vertices.index(source)+1:]) # tous les valeurs sauf le premier sommet (racine)
			#date = st.skewnorm.rvs(3, i, 5)
			#date = int(st.truncnorm.rvs( (borneInf - int(source[1])) / ecartType, (borneSup - int(source[1])) / ecartType, loc=int(source[1]), scale=ecartType ) )
			date = random.randint(borneInf, borneSup + 1)
			edges.append((source, dest, date, l))	# format arc : (source : str, dest : str, date : int, lambda l : int)
			print(i, "apres 7 :")

	return Multigraph(n, m, vertices, edges)




# Méthode permettant d'afficher un graphique de comparaison des performances ("temps de calcul" et "qualité des Solutions") de l'algorithme choisi
def plotPerformances(maxN, maxM, maxInterval_dates, nbTests, nbIterations, x, y, interval, save = False):
	ordonnee_tGlobal = []  # liste des temps de calcul moyen, vue globale sur le programme
	ordonnee_tInit = []  # liste des temps de calcul moyen, vue sur l'initialisation (transformation en graphe + calcul d'arbre couvrant)
	ordonnee_tType1 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type1
	ordonnee_tType2 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type2
	ordonnee_tType3 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type3
	ordonnee_tType4 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type4
	abscisse_n = []
	abscisse_m = []
	abscisse_interval_dates = []
	

	for nb in range(1, nbTests+1):
		n = int(maxN/nbTests*nb)
		m = int(maxM/nbTests*nb)
		interval_dates = [ int(maxInterval_dates[0]/nbTests*nb), int(maxInterval_dates[1]/nbTests*nb) ]

		abscisse_n.append(n)
		abscisse_m.append(m)
		abscisse_interval_dates.append(interval_dates)

		# Méthode permettant de générer des graphes aléatoires
		init_tStart = time.time() # init = initialisation programme = transformation en graphe + calcul d'arbre couvrant
		mg = randomMultigraphe(n, m, interval_dates)

		g = mg.transform_to_graph()
		g.show()

		p = MinimalDistanceProblem(g, x, y, interval)

		# voir si ajouter test sur arbres couvrants

		

		init_tEnd = time.time()
		ordonnee_tInit.append(init_tEnd - init_tStart)

		tGlobal = []
		tInit = []
		tType1 = []
		tType2 = []
		tType3 = []
		tType4 = []


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

			tGlobal.append(global_tEnd - global_tStart)
			tInit.append(init_tEnd - init_tStart)
			tType1.append(type1_tEnd - type1_tStart)
			tType2.append(type2_tEnd - type2_tStart)
			tType3.append(type3_tEnd - type3_tStart)
			tType4.append(type4_tEnd - type4_tStart)

			if verbose:
				print("Temps d'executions rélatifs à l'itération n.", ite, "\n\ttGlobal :", tGlobal, "\n\ttInit :", tInit, "\n\ttType1 :", tType1, "\n\ttType2 :", tType2, "\n\ttType3 :", tType3, "\n\ttType4 :", tType4)

		ordonnee_tGlobal.append( (sum(tGlobal)/len(tGlobal)) )
		ordonnee_tType1.append( (sum(tType1)/len(tType1)) )
		ordonnee_tType2.append( (sum(tType2)/len(tType2)) )
		ordonnee_tType3.append( (sum(tType3)/len(tType3)) )
		ordonnee_tType4.append( (sum(tType4)/len(tType4)) )

	if verbose:
		print("Temps d'executions moyens rélatifs au test n.", nb, "\n\tordonnee_tGlobal :", ordonnee_tGlobal, "\n\tordonnee_tInit :", ordonnee_tInit, "\n\tordonnee_tType1 :", ordonnee_tType1, "\n\tordonnee_tType2 :", ordonnee_tType2, "\n\tordonnee_tType3 :", ordonnee_tType3, "\n\tordonnee_tType4 :", ordonnee_tType4)
	
	
	#Affichage graphique
	plt.figure(figsize = (10, 10))
	plt.suptitle("Performances", size = 20, color = 'red')
	#plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
	
	# Construction et affichage du tracé "temps de calcul"
	#plt.subplot(3, 1, 1)
	plt.title("Analyse du temps de calcul en fonction du nombre de sommets n")
	plt.xlabel("n") # nombre de sommets du graphe G
	plt.ylabel("t(n)") # temps de calcul en fonction du nombre de sommets du graphe G
	plt.plot(abscisse_n, ordonnee_tGlobal, label = "temps Global")
	plt.plot(abscisse_n, ordonnee_tInit, label = "temps initialisation")
	plt.plot(abscisse_n, ordonnee_tType1, label = "type I : chemin d'arrivée au plus tôt")
	plt.plot(abscisse_n, ordonnee_tType2, label = "type II : chemin de départ au plus tard")
	plt.plot(abscisse_n, ordonnee_tType3, label = "type III : chemin le plus rapide")
	plt.plot(abscisse_n, ordonnee_tType4, label = "type VI : plus court chemin")
	plt.legend(loc='best')

	#plt.subplot(3, 1, 2)
	plt.title("Analyse du temps de calcul en fonction du nombre d'arcs m")
	plt.xlabel("m") # nombre d'arcs du graphe G
	plt.ylabel("t(m)") # temps de calcul en fonction du nombre d'arcs du graphe G
	plt.plot(abscisse_m, ordonnee_tGlobal, label = "temps Global")
	plt.plot(abscisse_m, ordonnee_tInit, label = "temps initialisation")
	plt.plot(abscisse_m, ordonnee_tType1, label = "type I : chemin d'arrivée au plus tôt")
	plt.plot(abscisse_m, ordonnee_tType2, label = "type II : chemin de départ au plus tard")
	plt.plot(abscisse_m, ordonnee_tType3, label = "type III : chemin le plus rapide")
	plt.plot(abscisse_m, ordonnee_tType4, label = "type VI : plus court chemin")
	plt.legend(loc='best')

	#plt.subplot(3, 1, 3)
	plt.title("Analyse du temps de calcul en fonction de l'intervalle de dates choisies interval_dates")
	plt.xlabel("interval_dates") # nombre de sommets du graphe G
	plt.ylabel("t(interval_dates)") # temps de calcul en fonction de l'interval de dates choisies du graphe G
	plt.plot(abscisse_interval_dates, ordonnee_tGlobal, label = "temps Global")
	plt.plot(abscisse_interval_dates, ordonnee_tInit, label = "temps initialisation")
	plt.plot(abscisse_interval_dates, ordonnee_tType1, label = "type I : chemin d'arrivée au plus tôt")
	plt.plot(abscisse_interval_dates, ordonnee_tType2, label = "type II : chemin de départ au plus tard")
	plt.plot(abscisse_interval_dates, ordonnee_tType3, label = "type III : chemin le plus rapide")
	plt.plot(abscisse_interval_dates, ordonnee_tType4, label = "type VI : plus court chemin")

	
	# Sauvegarde du tracé
	if (save):
		plt.savefig("TestResults/" + str(datetime.date.today()) + str(datetime.datetime.now().strftime("_%H_%M_%S")) + ".jpeg", transparent = True)
	
	plt.show()









def performances():
	
	maxN = 10
	maxM = 30
	maxInterval_dates = [0, 30]
	nbTests = 1
	nbIterations = 1
	x = "s0"
	y = "s" + str(maxN-1)
	interval = maxInterval_dates
	save = False
	
	plotPerformances(maxN, maxM, maxInterval_dates, nbTests, nbIterations, x, y, interval, save)
	
performances()