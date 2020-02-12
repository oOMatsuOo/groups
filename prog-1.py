import math
import pygame
import sys

# Constantes

BLEUCLAIR = (127, 191, 255)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
NOIR = (0, 0, 0)

K = 8.9876 * 10e9

A = 2
B = 5
C = 20

# Paramètres

dimensions_fenetre = (1600, 900)  # en pixels
images_par_seconde = 25

# Fonctions

def deplacer_pol(point, distance, orientation):
    x, y = point
    xf = x + (math.cos(orientation)*distance)
    yf = y + (math.sin(orientation)*distance)
    return (xf, yf)


def dessiner_vecteur(fenetre, couleur, origine, vecteur):
    alpha = math.atan2(vecteur[1], vecteur[0])
    norme_vecteur = math.sqrt(vecteur[0]**2 + vecteur[1]**2)
    if norme_vecteur >= C:
        p4 = (origine[0] + vecteur[0], origine[1] + vecteur[1])
        p1 = deplacer_pol(origine, A, alpha - (math.pi//2))
        p7 = deplacer_pol(origine, A, alpha + (math.pi//2))
        p2 = deplacer_pol(p1, norme_vecteur - C, alpha)
        p6 = deplacer_pol(p7, norme_vecteur - C, alpha)
        p3 = deplacer_pol(p2, B, alpha - (math.pi//2))
        p5 = deplacer_pol(p6, B, alpha + (math.pi//2))
        polygone = [p1, p2, p3, p4, p5, p6, p7]
    else:
        p3 = origine + vecteur
        p1 = deplacer_pol(p3, C, alpha + math.pi)
        p2 = deplacer_pol(p1, A+B, alpha - (math.pi//2))
        p4 = deplacer_pol(p1, A+B, alpha + (math.pi//2))
        polygone = [p1, p2, p3, p4]

    pygame.draw.polygon(fenetre, couleur, polygone)

    return

def ajouter_objet(x, y, q):
    objets.append((x, y, q))

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def calculer_champ(x, y):
    norme_vecteur = 0
    vecteur = [0, 0]
    angle = 0
    for l in objets:
        if y == l[1] and x == l[0]:
            return None
        if y!=l[1] or x!=l[0]:
            norme_vecteur = K * abs(l[2])/(distance(l[0], l[1], x, y)**2)
            angle = math.atan2(y - l[1],x - l[0])
            if l[2]>0:
                vecteur[0] += math.cos(angle) * norme_vecteur
                vecteur[1] += math.sin(angle) * norme_vecteur
            else:
                vecteur[0] -= math.cos(angle) * norme_vecteur
                vecteur[1] -= math.sin(angle) * norme_vecteur
    return vecteur

# Dessin
def dessiner_objet():
    for l in objets:
        if l[2]>0:
            pygame.draw.circle(fenetre, ROUGE, (l[0], l[1]), 10)
        else:
            pygame.draw.circle(fenetre, NOIR, (l[0], l[1]), 10)

def dessiner_champ():
    for x in range(-50, 1650, 50):
        for y in range(-50, 950, 50):
            vecteur = calculer_champ(x, y)
            if vecteur != None:
                norme_vecteur = distance(vecteur[0], vecteur[1], 0, 0)
                if norme_vecteur > 10e-10:
                    vecteur[0] *= 40/norme_vecteur
                    vecteur[1] *= 40/norme_vecteur
                    dessiner_vecteur(fenetre, BLEU, (x, y), vecteur)



# Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 1")

horloge = pygame.time.Clock()
couleur_fond = BLEUCLAIR

objets = []
ajouter_objet(800, 200, 0.000001)
ajouter_objet(800, 700, -0.000001)

# Dessin

fenetre.fill(couleur_fond)
dessiner_objet()
dessiner_champ()

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    horloge.tick(images_par_seconde)
