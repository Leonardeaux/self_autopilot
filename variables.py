import numpy as np

# Taille jeu  1024 x 768
TOP = 33  # Prendre en compte la taille des bordures
LEFT = 2560  # Taille de l'ecran principal 2560
WIDTH = 1024  # Largeur du jeu = 1024
HEIGHT = 768  # Hauteur du jeu = 768

# Taille écran 2K
TOP_2K = 0
LEFT_2K = 0
WIDTH_2K = 2560
HEIGHT_2K = 1440 - TOP_2K

# Taille écran Assetto Corsa Competizione
TOP_ACC = 175
LEFT_ACC = 0
WIDTH_ACC = 2560
HEIGHT_ACC = int((1440 - TOP_ACC) * 0.81)

# Taille du chrono de trackamania
"""Not used anymore"""
TOP_CHR = int(HEIGHT - (HEIGHT * 0.08))
LEFT_CHR = int(WIDTH - (WIDTH * 0.57))
BOTTOM_CHR = int(HEIGHT - (HEIGHT * 0.02))
RIGHT_CHR = int(WIDTH - (WIDTH * 0.44))


# Resize des images pour les entrainements
IMG_RESIZING = (160, 120, 1)

# Nombre de classe en sortie
N_CLASS = 8

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

BOX = {'top': TOP, 'left': LEFT, 'width': WIDTH, 'height': HEIGHT}
