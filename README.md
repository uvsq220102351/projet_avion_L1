# projet_avion_L1
Notre modèle de remplissage repose sur deux dictionnaire:



- dictinnaire_passagers : avec ses 4 champs 

  * destination : couple (i_d, j_d) du siège destination

  * nb_bagages : designe le nombre de bagage du passager (entre 0 et 2)

  * position : couple (i, j) qui designe la position actuelle du passager lors de la simulation

  * color : la couleur que prend le rectangle qui représente le passager

- dictionnaire_cases : à une (case) position (i,j) associe le numéro du passager qui l'occupe (0 si la case (i, j) est vide)



Au cours de la simulation, on parcourt les passager (par leur numéro de 1 à 180): pour un passager numéro k donné, 

on accède à sa position (i, j) actuelle et sa destination (i_d, j_d) (via (i,j) = dictinnaire_passagers[k]["position"] et (i_d,j_d) = dictinnaire_passagers[k]["destination"] )

puis on teste si le passager est dans le couloirs avant le coffre des bagages, ou s'il est devant celui-ci, s'il a déposé ou pas ses bagage et s'il est entre les 3 sièges près de sa destination.

Dans chaque cas, ou bien on fait avancer le passager vers la position suivante à l'aide de la fonction avancer_vers_siege_vide, ou on fait echanger la position du passager k avec celle de son voisin si ce dernier l'empêche de rejoindre son siège

. Dans chaque cas, on modifie aussi le dictionnaire_cases : on fait occuper une case on y stockant le numéro du passager qui l'occupe, on on la libère si le passager change de position.

Enfin l'interface graphique, consiste en une fonction principale play() qui parcourt tous les passager et les fait avancer, puis appelle une fonction redessiner, qui efface l'ancienne grille, puis reddessine la nouvelle

en utilisant les informations stockées dans le dictionnaire_passagers: pour chaque passager, sa position nous sert à dessiner un réctangle avec la couleur portée par le passager. Il fallait faire attention que les indices j des passager commence de bas en haut, 

mais que l'ordonnée y de l'interface graphique commence de haut en bas, aussi que l'abscine x commence à 0 mais que notre indice i de passager commence à 1. D'ou les formules suivante: 

x = (i-1)*c

y = (Ny - j)*c

avec c designe la dimension d'un carré (le coté), Ny designe la taille selon y : Ny = 30

