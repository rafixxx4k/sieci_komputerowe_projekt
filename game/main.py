import pygame
import sys
from constants import WHITE, GRAY, DARK_GRAY, BLACK, WINDOW_WIDTH, LOGIN_WINDOW_WIDTH, WINDOW_HEIGHT, LOGIN_WINDOW_HEIGHT, FONT_SIZE
from login_ui_elements import draw_login_screen
from login_logic import LoginLogic


def login_window():
    # Inicjalizacja Pygame
    pygame.init()
    # Ustawienia okna
    screen = pygame.display.set_mode((LOGIN_WINDOW_WIDTH, LOGIN_WINDOW_HEIGHT))
    pygame.display.set_caption("Login to Game")

    clock = pygame.time.Clock()
    loginLogic = LoginLogic()
    while True:
        screen.fill(GRAY)

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                loginLogic.keyboard_handler(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                loginLogic.mouse_handler(event)
        loginLogic.draw_login_screen(screen)
        pygame.display.flip()
        clock.tick(30)
        if loginLogic.get_logged():
            break


def game_window():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Window")

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        # Tutaj dodaj logikę dla nowego okna gry

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


def main():
    global username, room_number, active_input
    login_window()
    # game_window()


if __name__ == "__main__":
    main()
