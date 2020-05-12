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

# Paramètres

dimensions_fenetre = (800, 600)  # en pixels
images_par_seconde = 25
distance_repere = dimensions_fenetre[1]//6 - 15

def position_moteur():
    x = dimensions_fenetre[0]//2 + math.cos(angle_moteur) * distance_repere
    y = dimensions_fenetre[1]//2 - math.sin(angle_moteur) * distance_repere

    return (int(x), int(y))

def affichage_moteur():
    position_repere = position_moteur()

    pygame.draw.rect(fenetre, ROUGE, (dimensions_fenetre[0]//4, dimensions_fenetre[1]//3, dimensions_fenetre[0]//4, dimensions_fenetre[1]//3), 0)
    pygame.draw.rect(fenetre, BLEU, (dimensions_fenetre[0]//2, dimensions_fenetre[1]//3, dimensions_fenetre[0]//4, dimensions_fenetre[1]//3), 0)
    pygame.draw.circle(fenetre, BLEUCLAIR, (dimensions_fenetre[0]//2, dimensions_fenetre[1]//2), dimensions_fenetre[1]//5, 0)
    pygame.draw.circle(fenetre, GRIS, (dimensions_fenetre[0]//2, dimensions_fenetre[1]//2), dimensions_fenetre[1]//6, 0)
    pygame.draw.circle(fenetre, NOIR, position_repere, 8, 0)

def maj_compteur_courant():
    global compteur, courant

    if compteur!=0:
        compteur -= 1
        courant = 1
    else:
        courant = 0
        
def affichage_courant():
    police = pygame.font.SysFont("monospace", 20)

    texte_courant = "Courant : {0:.2f} A".format(courant)

    image = police.render(texte_courant, True, NOIR)
    fenetre.blit(image, (50, 50))



pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 12")

horloge = pygame.time.Clock()
couleur_fond = BLEUCLAIR

fenetre.fill(couleur_fond)

pygame.key.set_repeat(10, 10)

while True:
    fenetre.fill(couleur_fond)

    maj_compteur_courant()

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_SPACE:
                compteur = 5
    

    affichage_moteur()
    affichage_courant()

    pygame.display.flip()
    horloge.tick(images_par_seconde)