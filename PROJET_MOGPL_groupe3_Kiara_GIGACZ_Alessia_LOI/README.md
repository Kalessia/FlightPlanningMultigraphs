Multigraph algorithms to find the shortest, fastest, earliest and latest flight combinations in order to arrive at a specified destination within a given time interval (variants of BFS and Dijkstra, linear program for Gurobi). Multigraph generator for testing purposes.

Lien Google Drive pour le rapport : https://drive.google.com/drive/folders/1ffEkrCCSTVz6hUQp-NSnf2f1dNkr2yCw?usp=sharing




---

Format des données en entrée : 

> n % nombre de sommets
> m % nombre d'arcs
> sommet 1 
> sommet 2
> ...
> sommet n
> arc 1 % sous la forme (u, v, t, lambda)
> arc 2
> ...
> arc m
> x
> y
> intervalle % sous la forme (t_alpha, t_omega)


Pour utiliser le programme : 

- Télécharger le dossier et se placer au niveau du fichier main.py

- Lancer le programme en saisissant les données sous le format indiqué ci-dessus

	- au clavier (dans le terminal) : 
		- Entrer "python main.py" (ou test_main.py)
		- Entrer les données ligne par ligne

	- par fichier : 
		- Placer le fichier contenant les données dans le répertoire courant
		- Entrer "python main.py < input.in" où input.in est le nom de votre fichier (Attention: ne marche pas avec PowerShell)
