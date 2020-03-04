# ------------------------------------------------------------------------
# Laboratoires de programmation mathématique et physique 2
# ------------------------------------------------------------------------
#
# Programme : 7 segments.
#
# ------------------------------------------------------------------------

import math
import pygame
import sys
import numpy as np

### Constante(s)

NOIR = (0, 0, 0)
GRIS = (200, 200, 200)
ROUGE = (255, 0, 0)


### Variables Globales

variable_memorisee = 0


def dessiner_arduino(sortie_arduino, sortie_CD4511, sortie_CD4028, sortie_bouton):
    fenetre.blit(image_arduino, pos_arduino)
    fenetre.blit(image_CD4511, pos_CD4511)
    fenetre.blit(image_bouton, pos_bouton)
    fenetre.blit(image_CD4028, pos_CD4028)


    for j in range(0, 2):
        if j == 0:
            off_ard = 285
            off_cd = 15
            pos_carte = pos_CD4511
            r = range(0, 4)

        if j == 1:
            off_ard = 194
            off_cd = 91
            pos_carte = pos_CD4028
            r = range(4, 8)

        for i in r:
            if sortie_arduino[i] == 0:
                couleur = NOIR
            else:
                couleur = ROUGE

            pygame.draw.line(fenetre, couleur, (pos_arduino[0] + 280, pos_arduino[1] + off_ard),
                            (pos_carte[0] + 7, pos_carte[1] + off_cd), 5)
            off_ard = off_ard + 14
            off_cd = off_cd + 19



    off_cd = 15
    off_aff = 5
    i = 0
    for i in range(0, 7):
        if sortie_CD4511[i] == 0:
            couleur = NOIR
        else:
            couleur = ROUGE
        pygame.draw.line(fenetre, couleur, (pos_afficheur[0] + 591, pos_afficheur[1] + off_aff),
                        (pos_CD4511[0] + 102, pos_CD4511[1] + off_cd), 5)
        off_aff = off_aff + 19
        off_cd = off_cd + 19


    if sortie_bouton == 0:
        couleur = NOIR
    else:
        couleur = ROUGE
    pygame.draw.line(fenetre, couleur, (pos_arduino[0] + 279, pos_arduino[1] + 353),
                        (pos_bouton[0] + 13, pos_bouton[1] + 13), 5)

    i = 0
    off_cd = (102, 111)
    off_aff = 44
    for i in range(0, 6):
        if sortie_CD4028[i] == 0:
            couleur = NOIR
        else:
            couleur = ROUGE
        pygame.draw.line(fenetre, couleur, (pos_CD4028[0] + off_cd[0], pos_CD4028[1] + off_cd[1]),
                        (pos_afficheur[0] + off_aff, pos_CD4028[1] + off_cd[1]), 5)

        pygame.draw.line(fenetre, couleur, (pos_afficheur[0] + off_aff, pos_afficheur[1]),
                        (pos_afficheur[0] + off_aff, pos_CD4028[1] + off_cd[1] - 2), 5)
        off_cd = (off_cd[0], off_cd[1] - 20)
        off_aff = off_aff + 101



def dessiner_afficheur(sortie_CD4511, sortie_CD4028):
    positions_barres = [[32, 14], [89, 20], [87, 88], [28, 150],
                        [17, 88], [19, 20], [30, 82]]

    for j in range(0, 6):
        fenetre.blit(image_afficheur_s, (pos_afficheur[0] + j*101, pos_afficheur[1]))
        if sortie_CD4028[j] == 1:
            i = 0
            for barre in positions_barres:
                if sortie_CD4511[i] == 0:
                    i = i + 1
                    continue
                x_b = j*101 + pos_afficheur[0] + int(round(barre[0]*(image_afficheur_s.get_width()/133)))
                y_b = pos_afficheur[1] + int(round(barre[1]*(image_afficheur_s.get_height()/192)))
                if i == 0 or i == 3 or i == 6:
                    fenetre.blit(barre_horizontale_s, (x_b, y_b))
                else:
                    fenetre.blit(barre_verticale_s, (x_b, y_b))
                i = i + 1
    return

def dessiner_cercle():
    couleur = NOIR
    if sig_horloge == 1:
        couleur = ROUGE
    
    pygame.draw.circle(fenetre,couleur, pos_afficheur, 10)

def composant_CD4511(entree):
    tdv = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]

    tdv[0] = [1,1,1,1,1,1,0]
    tdv[1] = [0,1,1,0,0,0,0]
    tdv[2] = [1,1,0,1,1,0,1]
    tdv[3] = [1,1,1,1,0,0,1]
    tdv[4] = [0,1,1,0,0,1,1]
    tdv[5] = [1,0,1,1,0,1,1]
    tdv[6] = [1,0,1,1,1,1,1]
    tdv[7] = [1,1,1,0,0,0,0]
    tdv[8] = [1,1,1,1,1,1,1]
    tdv[9] = [1,1,1,1,0,1,1]

    nmb = 0

    for i in range(0,4):
        nmb += entree[i] * 2**abs(i-3)
        
    return np.array(tdv[nmb])

def sortie_memorisee():

    val = variable_memorisee

    nmb_bin = [0,0,0,0]

    for i in range (0,4):
        nmb_bin[i] = (val % 2)
        val = val // 2

    nmb_bin.reverse()

    return np.array(nmb_bin)

def gerer_click():
    return 0

def clique_bouton():
    global variable_memorisee
    souris_pos = pygame.mouse.get_pos()
    
    if souris_pos[0] >= pos_centre_bouton[0]-rayon_bouton and souris_pos[0] <= pos_centre_bouton[0] + rayon_bouton:
        if souris_pos[1] >= pos_centre_bouton[1]-rayon_bouton and souris_pos[1] <= pos_centre_bouton[1] + rayon_bouton:
            variable_memorisee = (variable_memorisee + 1) % 10
            return 1
    return 0

def connexion_bouton(sortie_bouton):
    couleur_ligne = NOIR
    if sortie_bouton == 1:
        couleur_ligne = ROUGE

    pygame.draw.line(fenetre,couleur_ligne, pin_arduino, pin_bouton, 6)
    return

### Paramètre(s)

dimensions_fenetre = (1100, 600)  # en pixels
images_par_seconde = 25

pos_arduino = (0, 70)
pos_CD4511 = (333, 340)
pos_CD4028 = (333, 128)
pos_afficheur = (500, 350)
pos_bouton = (333, 524)
pos_centre_bouton = (pos_bouton[0] + 51, pos_bouton[1] + 34)
rayon_bouton = 18
pin_arduino = (pos_arduino[0] + 279, pos_arduino[1] + 353)
pin_bouton = (pos_bouton[0] + 13, pos_bouton[1] + 13)

sig_horloge = 0


### Programme

# Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 7 segments")

horloge = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 500)

image_afficheur_s = pygame.image.load('images/7_seg_s.png').convert_alpha(fenetre)
barre_verticale_s = pygame.image.load('images/vertical_s.png').convert_alpha(fenetre)
barre_horizontale_s = pygame.image.load('images/horizontal_s.png').convert_alpha(fenetre)
image_afficheur = pygame.image.load('images/7_seg.png').convert_alpha(fenetre)
barre_verticale = pygame.image.load('images/vertical.png').convert_alpha(fenetre)
barre_horizontale = pygame.image.load('images/horizontal.png').convert_alpha(fenetre)
image_arduino = pygame.image.load('images/arduino.png').convert_alpha(fenetre)
image_CD4511 = pygame.image.load('images/CD4511.png').convert_alpha(fenetre)
image_CD4028 = pygame.image.load('images/CD4028.png').convert_alpha(fenetre)
image_bouton = pygame.image.load('images/bouton.png').convert_alpha(fenetre)
couleur_fond = GRIS



# Boucle principale


while True:
    temps_maintenant = pygame.time.get_ticks()
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            if clique_bouton():
                sortie_bouton = 1
            else:
                sortie_bouton = 0
        elif evenement.type == pygame.USEREVENT:
            sig_horloge = (sig_horloge + 1) % 2
            if sig_horloge == 1:
                variable_memorisee = (variable_memorisee + 1 ) % 10

    sortie_bouton = 0

    if pygame.mouse.get_pressed()[0]:
            sortie_bouton = 1

    fenetre.fill(couleur_fond)

    dessiner_arduino(np.zeros(8, dtype=int), np.zeros(7, dtype=int),
                 np.zeros(6, dtype=int), 0)
    dessiner_afficheur(np.zeros(7, dtype=int), np.zeros(6, dtype=int))

    pygame.display.flip()
    horloge.tick(images_par_seconde)