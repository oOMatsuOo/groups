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

# Paramètres

dimensions_fenetre = (1600, 900)  # en pixels
images_par_seconde = 25

# Fonctions

def ajouter_objet(x, y, q):
    objets.append((x, y, q))

def retirer_objet(x,y):
    for l in objets:
        if l[0] <= x + 5 and l[0] >= x - 5 and y <= l[1] + 5 and y >= l[1] - 5:
            objets.remove(l)

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculer_champ(x, y):
    norme_vecteur = 0
    vecteur = [0, 0]
    angle = 0
    for l in objets:
        if y >= l[1] - 25 and y <= l[1] + 25 and x >= l[0] - 25 and x <= l[0] + 25:
            return None
        elif y!=l[1] or x!=l[0]:
            norme_vecteur = K * abs(l[2])/(distance(l[0], l[1], x, y)**2)
            angle = math.atan2(y - l[1],x - l[0])
            if l[2]>0:
                vecteur[0] += math.cos(angle) * norme_vecteur
                vecteur[1] += math.sin(angle) * norme_vecteur
            else:
                vecteur[0] -= math.cos(angle) * norme_vecteur
                vecteur[1] -= math.sin(angle) * norme_vecteur
    return vecteur

def initialiser_mobile():
    global mobile_est_present

    mobile_est_present = False

    mobile = [0,0,0,0,1] # 0 : X; 1 : Y; 2 : Vx; 3 : Vy; 4 : charge

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
    v_champ = calculer_champ(mobile[0], mobile[1])
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

def calculer_energie_potentiel(x, y, charge):
    energ_pot = 0
    for l in objets:
        if x!=l[0] or y!=l[1]:
            energ_pot += K * (charge * l[2])/(distance(x, y, l[0], l[1]))
        else:
            return 0
    return energ_pot

def calculer_potentiel(x, y):
    if mobile_est_present:
        potent = calculer_energie_potentiel(x, y, 1) + K * mobile[4]/distance(x, y, mobile[0], mobile[1])
    else:
        potent = calculer_energie_potentiel(x, y, 1)
    return potent

# Dessin

def dessiner_objet():
    for l in objets:
        if l[2]>0:
            pygame.draw.circle(fenetre, ROUGE, (l[0], l[1]), 10)
        else:
            pygame.draw.circle(fenetre, NOIR, (l[0], l[1]), 10)

def dessiner_mobile():
    if mobile[4] > 0:
        couleur = ROUGE
    else:
        couleur = NOIR

    pygame.draw.circle(fenetre,couleur, (int(mobile[0]), int(mobile[1])), 10, 4)

def affichage_tableau():
    police = pygame.font.SysFont("monospace", 32)

    pot_elec = calculer_potentiel(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    texte_pot_elec = "Potentiel souris : {0:.2f} µJ".format(pot_elec)
    image = police.render(texte_pot_elec, True, NOIR)
    fenetre.blit(image, (50, 140))

    if not mobile_est_present:
        return
    ener_pot = calculer_energie_potentiel(mobile[0], mobile[1], mobile[4])*1e6
    ener_cine = (MASSE_MOBILE * distance(0, 0, mobile[2], mobile[3])**2)*1e6/2
    ener_tot = ener_pot + ener_cine

    texte_ener_pot = "Energie potentielle : {0:.2f} µJ".format(ener_pot)
    texte_ener_cinetique = "Energie cinetique : {0:.2f} µJ".format(ener_cine)
    texte_ener_tot = "Energie totale : {0:.2f} µJ".format(ener_tot)

    image = police.render(texte_ener_pot, True, NOIR)
    fenetre.blit(image, (50, 50))
    image = police.render(texte_ener_cinetique, True, NOIR)
    fenetre.blit(image, (50, 80))
    image = police.render(texte_ener_tot, True, NOIR)
    fenetre.blit(image, (50, 110))

    

# Intéraction

def traiter_souris(evenement):
    if evenement.button == 1:
        ajouter_objet(evenement.pos[0],evenement.pos[1], 1e-7)
    elif evenement.button == 3:
        ajouter_objet(evenement.pos[0],evenement.pos[1], -1e-7)
    elif evenement.button == 2:
        retirer_objet(evenement.pos[0], evenement.pos[1])
    return

# Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 3")

horloge = pygame.time.Clock()
couleur_fond = BLEUCLAIR

objets = []

ajouter_objet(800, 200, 1e-6)
ajouter_objet(800, 700, 1e-6)


# Dessin

fenetre.fill(couleur_fond)
dessiner_objet()
mobile = initialiser_mobile()
temps_precedent = 0


while True:
    temps_maintenant = pygame.time.get_ticks()

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            traiter_souris(evenement)
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_p:
                creer_mobile(1e-7,pygame.mouse.get_pos())
            elif evenement.key == pygame.K_n:
                creer_mobile(-1e-7,pygame.mouse.get_pos())
    



    fenetre.fill(couleur_fond)
    dessiner_objet()
    
    for t in range(temps_precedent, temps_maintenant - 1, 1):
        mettre_a_jour_mobile(t/1000)
        
    if mobile_est_present:
        dessiner_mobile()
    affichage_tableau()
    temps_precedent = temps_maintenant
    

    pygame.display.flip()
    horloge.tick(images_par_seconde)