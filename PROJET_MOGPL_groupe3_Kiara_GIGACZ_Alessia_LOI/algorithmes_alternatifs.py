from multigraph import *
from minimalDistanceProblem import *
import pandas as pd


def transformationMultigrapheListeAdjacence(multiG, verbose=False):
	"""
	Méthode permettant de transformer un multigraphe G pondéré par le temps en un graphe G' classique (modelisation : liste d'adjacence)

	multiG : multigraphe pondéré par le temps, structure Multigraph
	verbose : mettre à True pour visualiser le détail du déroulement de cet algorithme
	"""
	vIN = []
	vOUT = []
	for arc in multiG.edges :
		x = arc.split("(")[1].split(")")[0].split(",")

		# vIN(sommet multiGraphe) = liste de doublets (v, t) avec v = sommet multiGraphe et t = poids (date) de l'arc entrant de v + lambda
		newSommet = (x[1], int(x[2])+int(x[3]))
		if newSommet not in vIN:
			vIN.append(newSommet)

		# vOUT(sommet multiGraphe) = liste de doublets (v, t) avec v = sommet multiGraphe et t = poids (date) de l'arc sortant de v
		newSommet = (x[0], int(x[2]))
		if newSommet not in vOUT:
			vOUT.append(newSommet)

	# ensV = union des ensembles vIN et vOUT
	ensV = vIN + vOUT
	ensV.sort(key = operator.itemgetter(0, 1), reverse=False)

	# Construction de la liste d'adjacence listeAdj[key=source][val=destination, poids] (dictionnaire) du graphe G issu du multigraphe multiG
	ensE = []
	listeAdj = {}

	# Ajout des arcs du sommet source au sommet destination de poids 0
	ensV_copy = copy.deepcopy(ensV)
	prec = None
	while (len(ensV_copy) > 0):
		sommetEnsV = ensV_copy.pop(0)
		listeAdj[sommetEnsV] = []
		if (prec != None and prec[0] == sommetEnsV[0]) :
			ensE.append((prec,sommetEnsV, 0))
			listeAdj[prec].append((sommetEnsV, 0))

			if verbose :
				print("Ajout d'un arc de poids 0 entre ", prec, "et", sommetEnsV)

		prec = sommetEnsV

	# Ajout des arcs du sommet source au sommet destination de poids lambda
	for arc in multiG.edges :
		x = arc.split("(")[1].split(")")[0].split(",")
		source = (x[0], int(x[2]))
		dest = (x[1], int(x[2])+int(x[3]))
		ensE.append((source,dest,int(x[3])))
		listeAdj[source].append((dest, int(x[3])))

		if verbose :
			print("Ajout d'un arc de poids lambda entre ", source, "et", dest)

	if verbose :
		print("\nListe d'adjacence :", listeAdj)

	return listeAdj

#-------------------------------------------------------------------------------------------------------------------

def affichageMatG(matG, ensV):
	df = pd.DataFrame(matG, index = ensV, columns = ensV)
	print("\nMatrice d'adjacence rélative au graphe classique G' obtenu par transformation du multigraphe pondéré par le temps G")
	print("NB. Les symboles '-' qui figurent sont en réalité des -1 dans la matrice, ils servent seulement à favoriser la lisibilité\n")
	df[df==-1] = "-"
	print(df, "\n")

#-------------------------------------------------------------------------------------------------------------------









def  algorithmes_alternatifs():
	




algorithmes_alternatifs()