import numpy as np


TOP = 33  # Prendre en compte la taille des bordures
LEFT = 2560  # Taille de l'ecran principal 2560
WIDTH = 1024  # Largeur du jeu = 1024
HEIGHT = 768  # Hauteur du jeu = 768


VERTICES_FIRST_PERSON = np.array([[0, HEIGHT * 0.85],
                                  [0, HEIGHT * 0.6666],
                                  [WIDTH / 3, HEIGHT * 0.4],
                                  [WIDTH * 0.6666, HEIGHT * 0.4],
                                  [WIDTH, HEIGHT * 0.6666],
                                  [WIDTH, HEIGHT * 0.85]], dtype=np.int32)


TOP_CHR = int(HEIGHT - (HEIGHT * 0.08))
LEFT_CHR = int(WIDTH - (WIDTH * 0.57))
BOTTOM_CHR = int(HEIGHT - (HEIGHT * 0.02))
RIGHT_CHR = int(WIDTH - (WIDTH * 0.44))


BOX = {'top': TOP, 'left': LEFT, 'width': WIDTH, 'height': HEIGHT}