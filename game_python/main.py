import socket
import pygame
import sys
from constants import (
    WHITE,
    GRAY,
    DARK_GRAY,
    BLACK,
    WINDOW_WIDTH,
    LOGIN_WINDOW_WIDTH,
    WINDOW_HEIGHT,
    LOGIN_WINDOW_HEIGHT,
    FONT_SIZE,
)
from LoginLogic import LoginLogic
from GameLogic import GameLogic


def login_window(client_socket):
    """
    Displays the login window and handles user input for login.

    Args:
        client_socket (socket.socket): The client socket for communication with the server.

    Returns:
        int: The player ID after successful login.
    """
    pygame.init()
    screen = pygame.display.set_mode((LOGIN_WINDOW_WIDTH, LOGIN_WINDOW_HEIGHT))
    pygame.display.set_caption("Login to Game")

    clock = pygame.time.Clock()
    loginLogic = LoginLogic(client_socket)
    while True:
        screen.fill(GRAY)
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
        if loginLogic.get_logged() > 0:
            return loginLogic.get_logged()


def game_window(client_socket, me):
    """
    Displays the game window and handles user input for gameplay.

    Args:
        client_socket (socket.socket): The client socket for communication with the server.
        me (int): The player ID.

    Returns:
        None
    """
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Game Window")

    clock = pygame.time.Clock()
    gameLogic = GameLogic(me, client_socket)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gameLogic.mouse_handler(event)
        screen.fill(WHITE)
        gameLogic.draw_game_seen(screen)
        if gameLogic.get_winner():
            gameLogic.draw_end_seen(screen)
        pygame.display.flip()
        clock.tick(30)


def main(ip, port):
    """
    The main function that initializes the client socket, handles login and starts the game.

    Args:
        ip (str): The IP address of the server.

    Returns:
        None
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        me = 1
        me = login_window(client_socket)
        game_window(client_socket, me)

        client_socket.close()
    except Exception as e:
        print(f"Błąd podczas połączenia z serwerem: {e}")


def check_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


if __name__ == "__main__":
    # use ip address and port of the server as arguments

    if len(sys.argv) > 3:
        print("Usage: python3 main.py [ip_address] [port]")
        sys.exit()

    ip = sys.argv[1] if len(sys.argv) >1 else '127.0.0.1'

    port = int(sys.argv[2]) if len(sys.argv) == 3 else 1100

    if not check_ip(ip):
        print("Invalid ip address")
        sys.exit()

    if not 1024 <= port <= 65535:
        print("Invalid port number")
        sys.exit()

    main(ip, port)
