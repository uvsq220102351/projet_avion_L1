#MIASHS TD02
#VEDEL Clément
#VO Tuong Minh
#KOUNDOUL Adama
#GUIBLAIN Vincent
#ROBIC Camélia
#Chene William
#lien :
#groupe n°4


from tkinter import *
import random
from random import shuffle

Nx = 7
Ny = 30
NB_PASSAGERS = (Nx-1)*Ny

# couleur de passaver avec 2 bagages à main   
VIOLET  = 2 
# couleur de passager avec 1 bagage à main
MAGENTA = 1
# couleur de passager sans bagage à main avant d'arriver à destination
ROUGE   = 0
# couleur de passager arriver à sa destination
VERT    = -1

dictio_hexa_colors = {VIOLET : '#8E44AD',
                      VERT : '#2ECC71',
                      ROUGE : '#E74C3C',
                      MAGENTA : '#F1948A'}

def damier(): #fonction dessinant le tableau
    ligne_vert()
    ligne_hor()
        
def ligne_vert():
    c_x = 0
    while c_x != width:
        can1.create_line(c_x,0,c_x,height,width=1,fill='black')
        c_x+=c
        
def ligne_hor():
    c_y = 0
    while c_y != height:
        can1.create_line(0,c_y,width,c_y,width=1,fill='black')
        c_y+=c
        
def go():
    "démarrage de l'animation"
    global flag
    if flag ==0:
        flag =1
        play()
        
def stop():
    "arrêt de l'animation"
    global flag    
    flag =0

def generer_destinations():
    places = []
    for i in range(1, Nx+1):
        if i != 4:
            for j in range(1, Ny+1):
                places. append ((i, j))
    shuffle(places)
    return places

# on génère les places destinations des passagers aléatoirement
places = generer_destinations()


# fonction initialisation du dictionnaire des passagers : 
# - comporte la position du destination
# - le nombre de bagages : aléatoire entre 0 et 2
# - la position actuelle (4, 0)
# - la couleur du passager

def initialiser_dic_passagers():
    dictionnaire_passagers = {}
    position_nitiale    = (4, 0)
    
    for k in range(1, NB_PASSAGERS+1):
        # passager numéro k
        destination = places[k-1]
        nb_bagages  = random.randint(0,2)
        color       = nb_bagages
        
        dictionnaire_passagers[k] = {"destination": destination,
                                      "nb_bagages" : nb_bagages,
                                      "position"   : position_nitiale,
                                      "color"      : color
                                    }
    return dictionnaire_passagers

# on initialise le dictionnaire des passagers
dictionnaire_passagers = initialiser_dic_passagers()

VIDE = 0
def initialiser_dic_cases():
    dictionnaire_cases = {}
    for i in range(1, Nx+1):
        for j in range(1, Ny+1):
            dictionnaire_cases[(i,j)] = VIDE
    return dictionnaire_cases
dictionnaire_cases = initialiser_dic_cases()

# k numéro du passager
# i et j les coordonnées de sa position
# pas est le pas (+1 ou -1)
def avancer_vers_siege_vide(k, passager_k, i, j, pas):
    # on libère sa position actuelle
    dictionnaire_cases[i , j] = VIDE
    # la case suivante sera occupée par le passager
    dictionnaire_cases[i + pas, j] = k
    passager_k["position"] = (i + pas, j)
    if passager_k["position"] == passager_k["destination"]:
        passager_k["color"] = VERT
    # on met à jour les infos du passager k
    dictionnaire_passagers[k] = passager_k

                
#
def echanger_passagers(k, passager_k, k2, i, j, pas):
    
    passager_k2 = dictionnaire_passagers[k2]
    i_d2, j_d2 = passager_k2["destination"]
    i_d, j_d = passager_k["destination"]
    
    # on n'échange que si le passager k2 empêche le passager k d'aller à sa place
    if pas*(i_d - i_d2) > 0 :
        
        passager_k2["color"] = ROUGE

        passager_k2["position"] = (i, j)
        #dictionnaire_cases[i, j] = k2
        passager_k["position"] = (i + pas, j)
        #dictionnaire_cases[i + pas, j] = k
        # echange de numéro
        dictionnaire_passagers[k]  = passager_k2
        dictionnaire_passagers[k2] = passager_k
                
# on fait avancer le passager numéro k
def avancer_passager(k, liste_deja_traite):
    # on accède au infos du passager k en tête de la liste des passagers
    passager_k = dictionnaire_passagers[k]
    # on accède à sa position actuelle avant d'avancer
    i, j = passager_k["position"]
    # position finale : destination
    i_d, j_d = passager_k["destination"]
    
    if (i, j) != (i_d, j_d):
        # le passager n'est pas encore arrivé à sa destination
        
        # on calcule le pas : son signe indique la direction gauche ou droite
        
        if i_d > 4 :
            pas = 1
        else :
            pas = -1
        
        # Dans le couloir avant le niveau du siège: on avance dans le couloir
        if (i == 4) and (j < j_d) and (dictionnaire_cases[i, j+1] == VIDE):
            # le passager libère la position (i,j) actuelle et occupe la position (i, j+1)
            dictionnaire_cases[i, j] = VIDE
            dictionnaire_cases[i, j+1] = k
            passager_k["position"] = (i, j+1)
            # on met à jour les infos du passager k
            dictionnaire_passagers[k] = passager_k
            
            
        # Dans le couloir au niveau du siège : on dépose bagage par bagage
        elif (i == 4) and (j == j_d) and passager_k["nb_bagages"] > 0:
            passager_k["nb_bagages"] -= 1
            passager_k["color"] = passager_k["nb_bagages"]
            # on met à jour les infos du passager k
            dictionnaire_passagers[k] = passager_k

            
        # Après avir déposé les bagages
        # alors il commence à rejoindre son siège
        elif (i == 4) and (j == j_d) and passager_k["nb_bagages"] == 0:
            # on teste si le premier siège est libre : le passager avance vers ce siège
            if dictionnaire_cases[i + pas, j] == VIDE:
                avancer_vers_siege_vide(k, passager_k, i, j, pas)
                
            # sinon le passager echange de place avec l'occupant de ce siège
            else:
                k2 = dictionnaire_cases[i + pas, j]
                echanger_passagers(k, passager_k, k2, i, j, pas)
                liste_deja_traite.append(k)
                liste_deja_traite.append(k2)

        # si le passager se trouve en dehors du couloir : sur l'un des 3 siège mais qu'il n'est pas encore arrivé à sa derstination
        elif (i != 4) and (j == j_d):
            # si le prochain siège est vide, il avance vers ce siège
            if dictionnaire_cases[i + pas, j] == VIDE:
                avancer_vers_siege_vide(k, passager_k, i, j, pas)
            # sinon il échange la place avec l'occupant de ce prochain siège
            else:
                k2 = dictionnaire_cases[i + pas, j]
                echanger_passagers(k, passager_k, k2, i, j, pas)
                liste_deja_traite.append(k)
                liste_deja_traite.append(k2)
                
def play(): #fonction qui fait avancer les passager et redessine la grille
    global flag, vitesse
    
    # liste dans laquelle on ajoute certain passager deja traité
    liste_deja_traite = []
    # parcourir les passagers et modifier les dictionnaires
    for k in range(1, NB_PASSAGERS+1):
        if k not in liste_deja_traite:
            avancer_passager(k, liste_deja_traite)
            
    # redessiner
    redessiner()
    if flag >0: 
        fen1.after(vitesse,play)
        

def redessiner(): #fonction redessinant la grille à partir du dictionnaire dictionnaire_passagers
    
    # on éfface l'ancienne grille
    can1.delete(ALL)
    # on dessine le nouveau tableau
    damier()
    
    # on parcout les passager
    for k in range(1, NB_PASSAGERS+1):
        # on accède à leur position
        i, j = dictionnaire_passagers[k]["position"]
        # on accède à leur couleur : selon s'il portent des bagages ou s'ils sont à leur places
        color = dictionnaire_passagers[k]["color"]
        
        # on convertit le code couleur en code hexadecimal: à l'aide du dictionnaire dictio_hexa_colors
        hexa_color = dictio_hexa_colors[color]
        
        # on calcule les coordonnées du rectangle qu'on va déssiner
        x = (i-1)*c
        y = (Ny - j)*c
        
        # on crée le réctangle
        can1.create_rectangle(x, y, x+c, y+c, fill=hexa_color)
        
        
# taille de la grille
height = Ny*20
width  = 140

#taille des sièges
c = 20

#vitesse de l'animation (en réalité c'est l'attente entre chaque étapes en ms)
vitesse=500 

flag=0

#programme "principal" 
fen1 = Tk()

can1 = Canvas(fen1, width =width, height =height, bg ='white')
can1.pack(side =BOTTOM, padx =50, pady =50)

damier()

b1 = Button(fen1, text ='Go!', command =go)
b2 = Button(fen1, text ='Stop', command =stop)
b1.pack(side =LEFT, padx =3, pady =3)
b2.pack(side =LEFT, padx =3, pady =3)

fen1.mainloop()