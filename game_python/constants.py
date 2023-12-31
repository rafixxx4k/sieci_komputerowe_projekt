from threading import Semaphore

# Kolory
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
DARK_GRAY = (80, 80, 80)
BLACK = (0, 0, 0)

# Szerokość i wysokość okna
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
LOGIN_WINDOW_WIDTH = 400
LOGIN_WINDOW_HEIGHT = 300

# Czcionka
FONT_SIZE = 36
FONT_SIZE_SMALL = 26

# Port i host
PORT = 1100
HOST = "127.0.0.1"

# Semafory
UPDATE_SEMAPHORE = Semaphore(1)
