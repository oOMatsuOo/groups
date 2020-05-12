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
GRIS = (115, 115, 115)

angle_moteur = math.pi/4
compteur = 0
courant = 0
vitesse_moteur = 0
tension_moteur = 0
circuit_est_ouvert = True

K = 1000
R = 0.02
L = 0.06
B = 0.5
J = 1
c = 0.2
Rm = 10

# Paramètres

dimensions_fenetre = (800, 600)  # en pixels
images_par_seconde = 25
distance_repere = dimensions_fenetre[1]//6 - 15

def position_moteur():
    x = dimensions_fenetre[0]//2 + math.cos(angle_moteur) * distance_repere
    y = dimensions_fenetre[1]//2 - math.sin(angle_moteur) * distance_repere

    return (int(x), int(y))

def maj_compteur_courant():
    global tension_moteur

    if not circuit_est_ouvert:
        tension_moteur = 10
        angle = math.fmod(angle_moteur, 2*math.pi)
        if angle>=math.pi/2 and angle<=3*math.pi/2:
            tension_moteur *=-1
    else:
        tension_moteur = 0

def maj_moteur(t):
    global vitesse_moteur, angle_moteur, temps_prec, tension_moteur, courant

    E = 2*K*R*L*B*vitesse_moteur*math.cos(angle_moteur)

    if circuit_est_ouvert:
        courant = 0
        tension_moteur = E
    else:
        courant = 10-E/Rm
        angle = math.fmod(angle_moteur, 2*math.pi)
        if angle>=math.pi/2 and angle<=3*math.pi/2:
            courant *= -1

    tho_frottement = -c*vitesse_moteur
    tho = 2*K*R*L*courant*B*math.cos(angle_moteur) + tho_frottement

    alpha = tho/J

    delta_t = t - temps_prec

    vitesse_moteur += alpha*delta_t
    angle_moteur += vitesse_moteur*delta_t

    temps_prec = t


def affichage_moteur():
    position_repere = position_moteur()

    pygame.draw.rect(fenetre, ROUGE, (dimensions_fenetre[0]//4, dimensions_fenetre[1]//3, dimensions_fenetre[0]//4, dimensions_fenetre[1]//3), 0)
    pygame.draw.rect(fenetre, BLEU, (dimensions_fenetre[0]//2, dimensions_fenetre[1]//3, dimensions_fenetre[0]//4, dimensions_fenetre[1]//3), 0)
    pygame.draw.circle(fenetre, BLEUCLAIR, (dimensions_fenetre[0]//2, dimensions_fenetre[1]//2), dimensions_fenetre[1]//5, 0)
    pygame.draw.circle(fenetre, GRIS, (dimensions_fenetre[0]//2, dimensions_fenetre[1]//2), dimensions_fenetre[1]//6, 0)
    pygame.draw.circle(fenetre, NOIR, position_repere, 8, 0)
        
def affichage_tableau_bord():
    police = pygame.font.SysFont("monospace", 20)

    texte_courant = "Courant : {0:.2f} A".format(courant)
    texte_tension = "Tension : {0:.2f} V".format(tension_moteur)

    image = police.render(texte_courant, True, NOIR)
    fenetre.blit(image, (50, 50))
    image = police.render(texte_tension, True, NOIR)
    fenetre.blit(image, (50, 75))



pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 12")

horloge = pygame.time.Clock()
couleur_fond = BLEUCLAIR

fenetre.fill(couleur_fond)

pygame.key.set_repeat(10, 10)

temps_precedent = 0
temps_maintenant = pygame.time.get_ticks()
temps_prec = temps_maintenant/1000


while True:
    fenetre.fill(couleur_fond)
    temps_maintenant = pygame.time.get_ticks()

    maj_compteur_courant()
    for t in range(temps_precedent, temps_maintenant - 1, 1):
        maj_moteur(t/1000)
    circuit_est_ouvert = True
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_SPACE:
                circuit_est_ouvert = False
    

    affichage_moteur()
    affichage_tableau_bord()

    temps_precedent = temps_maintenant

    pygame.display.flip()
    horloge.tick(images_par_seconde)