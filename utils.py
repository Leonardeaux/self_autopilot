import numpy as np

TOP = 33  # Prendre en compte la taille des bordures
LEFT = 2560  # Taille de l'ecran principal 2560
WIDTH = 1024  # Largeur du jeu = 1024
HEIGHT = 768  # Hauteur du jeu = 768

VERTICES_FIRST_PERSON_F1 = np.array([[0, HEIGHT * 0.85],
                                     [0, HEIGHT * 0.6666],
                                     [WIDTH / 3, HEIGHT * 0.4],
                                     [WIDTH * 0.6666, HEIGHT * 0.4],
                                     [WIDTH, HEIGHT * 0.6666],
                                     [WIDTH, HEIGHT * 0.85]], dtype=np.int32)

VERTICES_FIRST_PERSON_SUPERCAR = np.array([[0, HEIGHT * 0.82],
                                           [0, HEIGHT * 0.5],
                                           [WIDTH / 3, HEIGHT * 0.45],
                                           [WIDTH * 0.6666, HEIGHT * 0.45],
                                           [WIDTH, HEIGHT * 0.5],
                                           [WIDTH, HEIGHT * 0.82]], dtype=np.int32)

VERTICES_THIRD_PERSON = np.array([[0, HEIGHT * 0.8],
                                  [0, HEIGHT * 0.57],
                                  [WIDTH * 0.3333, HEIGHT * 0.45],
                                  [WIDTH * 0.6666, HEIGHT * 0.45],
                                  [WIDTH, HEIGHT * 0.57],
                                  [WIDTH, HEIGHT * 0.8]], dtype=np.int32)
vertices = np.array(
    [[0, HEIGHT * 0.455],
     [WIDTH / 3, HEIGHT * 0.365],
     [WIDTH * 0.62, HEIGHT * 0.365],
     [WIDTH - 1, HEIGHT * 0.41],
     [WIDTH - 1, HEIGHT * 0.82],
     [WIDTH * 0.84, HEIGHT * 0.83],
     [WIDTH * 0.64, HEIGHT / 2],
     [WIDTH / 3, HEIGHT / 2],
     [WIDTH * 0.16, HEIGHT * 0.83],
     [0, HEIGHT * 0.83]], dtype=np.int32)

TOP_CHR = int(HEIGHT - (HEIGHT * 0.08))
LEFT_CHR = int(WIDTH - (WIDTH * 0.57))
BOTTOM_CHR = int(HEIGHT - (HEIGHT * 0.02))
RIGHT_CHR = int(WIDTH - (WIDTH * 0.44))

BOX = {'top': TOP, 'left': LEFT, 'width': WIDTH, 'height': HEIGHT}
