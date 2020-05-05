#Russe Cyril
#Randaxhe Martin
#Van Muysewinkel Kieran

import math
import pygame
import sys


# Constantes

BLEUCLAIR = (127, 191, 255)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
NOIR = (0, 0, 0)

K = 8.9876 * 1e9

A = 2
B = 5
C = 20


MASSE_MOBILE = 1e-10

charge_mobile = 1e-10

mobile_est_present = False

champs_elect_v = 10

champs_magnetique = 1

# Paramètres

dimensions_fenetre = (800, 600)  # en pixels
images_par_seconde = 25

# Fonctions

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculer_champ_elect(x, y):
    return (0,-champs_elect_v)

def initialiser_mobile():
    global mobile_est_present, temps_prec

    mobile_est_present = True

    mobile = [dimensions_fenetre[0]/2,dimensions_fenetre[1]/2,0,0,charge_mobile] # 0 : X; 1 : Y; 2 : Vx; 3 : Vy; 4 : charge
    temps_prec = temps_maintenant/1000

    return mobile

def creer_mobile(charge,position):
    global mobile_est_present, mobile, temps_prec

    mobile = [0,0,0,0,1]
    mobile_est_present = True
    mobile[4] = charge
    mobile[0] = position[0]
    mobile[1] = position[1]
    temps_prec = temps_maintenant/1000

def mettre_a_jour_mobile(t):
    global mobile, mobile_est_present, temps_prec
    if not mobile_est_present:
        return
    v_champ = calculer_champ_elect(mobile[0], mobile[1])
    if v_champ==None:
        mobile_est_present=False
        return
    force = [v_champ[0] * mobile[4], v_champ[1] * mobile[4]]
    acceleration = [force[0]/MASSE_MOBILE, force[1]/MASSE_MOBILE]
    delta_t = t - temps_prec

    mobile[2]+= acceleration[0] * delta_t
    mobile[3]+= acceleration[1] * delta_t
    
    mobile[0]+= mobile[2] * delta_t
    mobile[1]+= mobile[3] * delta_t
    temps_prec = t

# def calculer_energie_potentiel(x, y, charge):
#     energ_pot = 0
#     for l in objets:
#         if x!=l[0] or y!=l[1]:
#             energ_pot += K * (charge * l[2])/(distance(x, y, l[0], l[1]))
#         else:
#             return 0
#     return energ_pot

def calculer_potentiel(x, y):
    if mobile_est_present:
        potent = calculer_energie_potentiel(x, y, 1) + K * mobile[4]/distance(x, y, mobile[0], mobile[1])
    else:
        potent = calculer_energie_potentiel(x, y, 1)
    return potent

# Dessin

def dessiner_mobile():
    if mobile[4] > 0:
        couleur = ROUGE
    else:
        couleur = NOIR
    
    print(mobile)

    pygame.draw.circle(fenetre,couleur, (int(mobile[0]), int(mobile[1])), 10, 4)

def affichage_tableau():
    police = pygame.font.SysFont("monospace", 32)

    if not mobile_est_present:
        return

    champ_elect = champs_elect_v
    ener_cine = (MASSE_MOBILE * distance(0, 0, mobile[2], mobile[3])**2)*1e6/2

    texte_ener_pot = "Champ électrique : {0:.2f} V/m".format(champ_elect)
    texte_ener_cinetique = "Energie cinetique : {0:.2f} µJ".format(ener_cine)
    texte_champs_magnetique = "Champs magnétique : {0:.2f} T".format(champs_magnetique)

    image = police.render(texte_ener_pot, True, NOIR)
    fenetre.blit(image, (50, 50))
    image = police.render(texte_ener_cinetique, True, NOIR)
    fenetre.blit(image, (50, 80))
    image = police.render(texte_champs_magnetique, True, NOIR)
    fenetre.blit(image, (50, 110))

    return

    

# Intéraction

# Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 11")

horloge = pygame.time.Clock()
couleur_fond = BLEUCLAIR

mobile = []

# Dessin

fenetre.fill(couleur_fond)
temps_maintenant = pygame.time.get_ticks()
temps_precedent = 0
temps_prec = 0

mobile = initialiser_mobile()

while True:
    temps_maintenant = pygame.time.get_ticks()

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_p:
                creer_mobile(1e-7,pygame.mouse.get_pos())
            elif evenement.key == pygame.K_n:
                creer_mobile(-1e-7,pygame.mouse.get_pos())
            elif evenement.key == pygame.K_UP:
                champs_elect_v += 1
            elif evenement.key == pygame.K_DOWN:
                champs_elect_v -= 1
            elif evenement.key == pygame.K_SPACE:
                mobile = initialiser_mobile()

    fenetre.fill(couleur_fond)
    
    for t in range(temps_precedent, temps_maintenant - 1, 1):
        mettre_a_jour_mobile(t/1000)
        
    if mobile_est_present:
        dessiner_mobile()
    affichage_tableau()
    temps_precedent = temps_maintenant
    

    pygame.display.flip()
    horloge.tick(images_par_seconde)