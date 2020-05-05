#Russe Cyril
#Randaxhe Martin
#Van Muysewinkel Kieran

import math
import pygame
import sys


# Constantes

TAILLE_TRACE = 10000
trace = [(0, 0)] * TAILLE_TRACE
nb_trace = 0
prochain_trace = 0


BLEUCLAIR = (127, 191, 255)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
NOIR = (0, 0, 0)
GRIS = (115, 115, 115)

K = 8.9876 * 1e9

A = 2
B = 5
C = 20

a = 10


MASSE_MOBILE = 1e-10
charge_mobile = 1e-10
mobile_est_present = False

champs_elect_v = 10
champs_magnetique = 1

mode_cyclotron = False
alpha = 0

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

def initialiser_trace():
    global trace, nb_trace, prochain_trace

    nb_trace = 0
    prochain_trace = 0
    trace = [0] * TAILLE_TRACE

def ajouter_trace():
    global trace, nb_trace, prochain_trace

    if nb_trace < TAILLE_TRACE:
        nb_trace += 1

    trace[prochain_trace] = (mobile[0], mobile[1])
    prochain_trace = (prochain_trace+1)%TAILLE_TRACE

def afficher_trace():
    for i in range(0, nb_trace):
        pygame.draw.circle(fenetre, GRIS, (int(trace[i][0]), int(trace[i][1])), 4, 0)

def calculer_champ_cyclotron(dt):
    global alpha, champs_elect_v

    T = 2 * math.pi * MASSE_MOBILE / (charge_mobile * champs_magnetique)
    
    alpha += 2 * math.pi * dt / T
    alpha = math.fmod(alpha, 2 * math.pi)

    champs_elect_v = a * math.sin(alpha)


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

    delta_t = t - temps_prec

    if mode_cyclotron:
        calculer_champ_cyclotron(delta_t)

    norme_vitesse = distance(mobile[2], mobile[3], 0, 0)
    force_champ_magnetique = mobile[4] * norme_vitesse * champs_magnetique
    angle_vitesse = math.atan2(mobile[3], mobile[2])

    force = [v_champ[0] * mobile[4] + force_champ_magnetique * math.cos(angle_vitesse+math.pi/2), v_champ[1] * mobile[4] + force_champ_magnetique * math.sin(angle_vitesse+math.pi/2)]    
    
    acceleration = [force[0]/MASSE_MOBILE, force[1]/MASSE_MOBILE]
    

    mobile[2]+= acceleration[0] * delta_t
    mobile[3]+= acceleration[1] * delta_t
    
    mobile[0]+= mobile[2] * delta_t
    mobile[1]+= mobile[3] * delta_t
    temps_prec = t

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
initialiser_trace()

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
                mode_cyclotron = False
            elif evenement.key == pygame.K_DOWN:
                champs_elect_v -= 1
                mode_cyclotron = False
            elif evenement.key == pygame.K_SPACE:
                mobile = initialiser_mobile()
                initialiser_trace()
                mode_cyclotron = False
            elif evenement.key == pygame.K_PAGEUP and champs_magnetique < 1:
                champs_magnetique += 0.5
            elif evenement.key == pygame.K_PAGEDOWN and champs_magnetique > -1:
                champs_magnetique -= 0.5
            elif evenement.key == pygame.K_c:
                mode_cyclotron = True

    fenetre.fill(couleur_fond)
    
    for t in range(temps_precedent, temps_maintenant - 1, 1):
        mettre_a_jour_mobile(t/1000)
    
    ajouter_trace()

    if mobile_est_present:
        dessiner_mobile()
        afficher_trace()
    affichage_tableau()
    temps_precedent = temps_maintenant
    

    pygame.display.flip()
    horloge.tick(images_par_seconde)