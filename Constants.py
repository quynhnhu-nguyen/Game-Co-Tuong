import pygame

# User interface
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650

# Initial score
Start_X = 50
Start_Y = 50

# Length of each line
Line_Span = 60

player1Color = 1
player2Color = 2
overColor = 3

BG_COLOR = pygame.Color(213, 176, 146)      # Background color
Line_COLOR = pygame.Color(255, 255, 200)    # Line color
TEXT_COLOR = pygame.Color(255, 0, 0)        # Text color

# Define color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

repeat = 0

# Chess piece image
pieces_images = {
    # Black team
    'b_general': pygame.image.load("imgs/black/b_g.gif"),     # General
    'b_chariot': pygame.image.load("imgs/black/b_cha.gif"),     # Chariot
    'b_horse': pygame.image.load("imgs/black/b_h.gif"),        # Horse
    'b_cannon': pygame.image.load("imgs/black/b_can.gif"),     # Cannon
    'b_elephant': pygame.image.load("imgs/black/b_e.gif"),     # Elephant
    'b_advisor': pygame.image.load("imgs/black/b_a.gif"),       # Advisor
    'b_soldier': pygame.image.load("imgs/black/b_s.gif"),      # Soldier

    # Red team
    'r_general': pygame.image.load("imgs/red/r_g.gif"),
    'r_chariot': pygame.image.load("imgs/red/r_cha.gif"),
    'r_horse': pygame.image.load("imgs/red/r_h.gif"),
    'r_cannon': pygame.image.load("imgs/red/r_can.gif"),
    'r_elephant': pygame.image.load("imgs/red/r_e.gif"),
    'r_advisor': pygame.image.load("imgs/red/r_a.gif"),
    'r_soldier': pygame.image.load("imgs/red/r_s.gif"),
}

# Chess settings constant

# 2 player
my_max = True
my_min = False

# Eight pawns
invalid = 0
general = 1
chariot = 2
horse = 3
cannon = 4
elephant = 5
advisor = 6
soldier = 7

# Initialization table
init_borad = [
    [chariot,  invalid, invalid, soldier, invalid, invalid, soldier, invalid, invalid, chariot],
    [horse,    invalid, cannon,  invalid, invalid, invalid, invalid, cannon,  invalid, horse],
    [elephant, invalid, invalid, soldier, invalid, invalid, soldier, invalid, invalid, elephant],
    [advisor,  invalid, invalid, invalid, invalid, invalid, invalid, invalid, invalid, advisor],
    [general,  invalid, invalid, soldier, invalid, invalid, soldier, invalid, invalid, general],
    [advisor,  invalid, invalid, invalid, invalid, invalid, invalid, invalid, invalid, advisor],
    [elephant, invalid, invalid, soldier, invalid, invalid, soldier, invalid, invalid, elephant],
    [horse,    invalid, cannon,  invalid, invalid, invalid, invalid, cannon,  invalid, horse],
    [chariot,  invalid, invalid, soldier, invalid, invalid, soldier, invalid, invalid, chariot]
]

# Maximum number of steps
max_depth = 4

# Maximum - Minimum value
max_val = 1000000
min_val = -1000000

# Evaluation methods
base_val   = [0, 0, 500, 300, 300, 250, 250, 80]
mobile_val = [0, 0,   6,  12,   6,   1,   1, 15]
pos_val = [
    [  # Invalid
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ],
    [  # General
        0,  0,  0, 0, 0, 0, 0, 0, 0, 0,
        0,  0,  0, 0, 0, 0, 0, 0, 0, 0,
        0,  0,  0, 0, 0, 0, 0, 0, 0, 0,
        1, -8, -9, 0, 0, 0, 0, 0, 0, 0,
        5, -8, -9, 0, 0, 0, 0, 0, 0, 0,
        1, -8, -9, 0, 0, 0, 0, 0, 0, 0,
        0,  0,  0, 0, 0, 0, 0, 0, 0, 0,
        0,  0,  0, 0, 0, 0, 0, 0, 0, 0,
        0,  0,  0, 0, 0, 0, 0, 0, 0, 0
    ],
    [  # Chariot
        -6,  5, -2,  4,  8,  8,  6,  6,  6,  6,
         6,  8,  8,  9, 12, 11, 13,  8, 12,  8,
         4,  6,  4,  4, 12, 11, 13,  7,  9,  7,
        12, 12, 12, 12, 14, 14, 16, 14, 16, 13,
         0,  0, 12, 14, 15, 15, 16, 16, 33, 14,
        12, 12, 12, 12, 14, 14, 16, 14, 16, 13,
         4,  6,  4,  4, 12, 11, 13,  7,  9,  7,
         6,  8,  8,  9, 12, 11, 13,  8, 12,  8,
        -6,  5, -2,  4,  8,  8,  6,  6,  6,  6
    ],
    [  # Horse
         0,  -3, 5,  4,  2,  2,  5,  4,  2, 2,
        -3,   2, 4,  6, 10, 12, 20, 10,  8, 2,
         2,   4, 6, 10, 13, 11, 12, 11, 15, 2,
         0,   5, 7,  7, 14, 15, 19, 15,  9, 8,
         2, -10, 4, 10, 15, 16, 12, 11,  6, 2,
         0,   5, 7,  7, 14, 15, 19, 15,  9, 8,
         2,   4, 6, 10, 13, 11, 12, 11, 15, 2,
        -3,   2, 4,  6, 10, 12, 20, 10,  8, 2,
         0,  -3, 5,  4,  2,  2,  5,  4,  2, 2
    ],
    [  # Cannon
        0, 0, 1, 0, -1, 0, 0,  1,  2,  4,
        0, 1, 0, 0,  0, 0, 3,  1,  2,  4,
        1, 2, 4, 0,  3, 0, 3,  0,  0,  0,
        3, 2, 3, 0,  0, 0, 2, -5, -4, -5,
        3, 2, 5, 0,  4, 4, 4, -4, -7, -6,
        3, 2, 3, 0,  0, 0, 2, -5, -4, -5,
        1, 2, 4, 0,  3, 0, 3,  0,  0,  0,
        0, 1, 0, 0,  0, 0, 3,  1,  2,  4,
        0, 0, 1, 0, -1, 0, 0,  1,  2,  4
    ],
    [  # Elephant
        0, 0, -2, 0, 0, 0, 0, 0, 0, 0,
        0, 0,  0, 0, 0, 0, 0, 0, 0, 0,
        0, 0,  0, 0, 0, 0, 0, 0, 0, 0,
        0, 0,  0, 0, 0, 0, 0, 0, 0, 0,
        0, 0,  3, 0, 0, 0, 0, 0, 0, 0,
        0, 0,  0, 0, 0, 0, 0, 0, 0, 0,
        0, 0,  0, 0, 0, 0, 0, 0, 0, 0,
        0, 0,  0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, -2, 0, 0, 0, 0, 0, 0, 0
    ],
    [  # Advisor
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 3, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ],
    [  # Soldier
        0, 0, 0, -2, 3, 10, 20, 20, 20, 0,
        0, 0, 0,  0, 0, 18, 27, 30, 30, 0,
        0, 0, 0, -2, 4, 22, 30, 45, 50, 0,
        0, 0, 0,  0, 0, 35, 40, 55, 65, 2,
        0, 0, 0,  6, 7, 40, 42, 55, 70, 4,
        0, 0, 0,  0, 0, 35, 40, 55, 65, 2,
        0, 0, 0, -2, 4, 22, 30, 45, 50, 0,
        0, 0, 0,  0, 0, 18, 27, 30, 30, 0,
        0, 0, 0, -2, 3, 10, 20, 20, 20, 0
    ]
]