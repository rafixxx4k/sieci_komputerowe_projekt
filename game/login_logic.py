import pygame
import socket
from constants import WHITE, DARK_GRAY, BLACK, FONT_SIZE


class LoginLogic:
    """
    A class that handles the login logic for a game.

    Attributes:
    - me (int): The player's identifier.
    - username (str): The player's username.
    - room_number (str): The room number the player wants to join.
    - active_input (str): The currently active input field ("username" or "room_number").
    - font (pygame.font.Font): The font used for rendering text.
    - client_socket (socket.socket): The client socket used for communication.

    Methods:
    - send_credential(): Sends the player's credentials to the server.
    - keyboard_handler(event): Handles keyboard events for input handling.
    - mouse_handler(event): Handles mouse events for input handling.
    - draw_text(surface, text, x, y): Draws text on the given surface at the specified position.
    - draw_button(surface, text, x, y, width, height): Draws a button on the given surface with the specified properties.
    - draw_login_screen(screen): Draws the login screen on the given screen.
    - get_state(): Returns the current state of the login logic (username, room_number, active_input).
    - get_logged(): Returns the player's identifier.
    """

    def __init__(self, client_socket):
        self.me = 0
        self.username = ""
        self.room_number = ""
        self.active_input = "username"
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.client_socket = client_socket

    def send_credential(self):
        """
        Sends the player's credentials to the server.

        If the username is not empty and the room number is a 4-digit number,
        the credentials are sent to the server. The server's response is then
        processed to determine the player's identifier.

        If the room is full, a message is printed indicating that the room is full.
        If the credentials are invalid, a message is printed indicating that the
        data is incorrect.
        """
        if len(self.username) > 0 and len(self.room_number) == 4:
            print(f'user: {self.username}, room: {self.room_number}')
            message = f"{self.room_number:04}{self.username:<14}"
            self.client_socket.send(message.encode())
            rec = self.client_socket.recv(1024)
            rec = int(rec.decode())
            if rec > 0:
                self.me = rec
            else:
                print("Pokój do którego chcesz dołączyć jest pełen.")

            print(rec)
        else:
            print("Niepoprawne dane. Wprowadź poprawne dane.")

    def keyboard_handler(self, event):
        """
        Handles keyboard events for input handling.

        Args:
        - event (pygame.event.Event): The keyboard event.

        If the backspace key is pressed, the last character of the active input field
        is removed. If the tab key is pressed, the active input field is switched between
        "username" and "room_number". If the return key is pressed, the player's credentials
        are sent to the server. If the active input field is "username" and the username
        length is less than 14, the pressed character is added to the username. If the
        active input field is "room_number" and the room number length is less than 4,
        the pressed character is added to the room number.
        """
        if event.key == pygame.K_BACKSPACE:
            if self.active_input == "username" and len(self.username) > 0:
                self.username = self.username[:-1]
            elif self.active_input == "room_number" and len(self.room_number) > 0:
                self.room_number = self.room_number[:-1]
        elif event.key == pygame.K_TAB:
            if self.active_input == "username":
                self.active_input = "room_number"
            else:
                self.active_input = "username"
        elif event.key == pygame.K_RETURN:
            self.send_credential()

        elif self.active_input == "username" and len(self.username) < 14:
            self.username += event.unicode

        elif self.active_input == "room_number" and len(self.room_number) < 4:
            if event.unicode.isdigit():
                self.room_number += event.unicode

    def mouse_handler(self, event):
        """
        Handles mouse events for input handling.

        Args:
        - event (pygame.event.Event): The mouse event.

        Returns:
        - str: The updated active input field.

        If the mouse is clicked within the username input field, "username" is returned.
        If the mouse is clicked within the room number input field, "room_number" is returned.
        If the mouse is clicked on the "Dołącz" button, the player's credentials are sent
        to the server. Otherwise, the active input field remains unchanged.
        """
        if 50 <= event.pos[0] <= 350 and 50 <= event.pos[1] < 150:
            return "username"
        elif 50 <= event.pos[0] <= 350 and 150 <= event.pos[1] < 230:
            return "room_number"
        elif 250 <= event.pos[0] <= 340 and 230 <= event.pos[1] <= 265:
            self.send_credential()
        return self.active_input

    def draw_text(self, surface, text, x, y):
        """
        Draws text on the given surface at the specified position.

        Args:
        - surface (pygame.Surface): The surface to draw on.
        - text (str): The text to draw.
        - x (int): The x-coordinate of the text position.
        - y (int): The y-coordinate of the text position.
        """
        text_surface = self.font.render(text, True, BLACK)
        surface.blit(text_surface, (x, y))

    def draw_button(self, surface, text, x, y, width, height):
        """
        Draws a button on the given surface with the specified properties.

        Args:
        - surface (pygame.Surface): The surface to draw on.
        - text (str): The text to display on the button.
        - x (int): The x-coordinate of the button position.
        - y (int): The y-coordinate of the button position.
        - width (int): The width of the button.
        - height (int): The height of the button.
        """
        pygame.draw.rect(surface, DARK_GRAY, (x, y, width, height), 0, 5)
        pygame.draw.rect(surface, BLACK, (x, y, width, height), 2, 5)
        self.draw_text(surface, text, x+6, y+6)

    def draw_login_screen(self, screen):
        """
        Draws the login screen on the given screen.

        Args:
        - screen (pygame.Surface): The screen to draw on.

        The login screen consists of two input fields for username and room number,
        and a "Conect" button. The active input field is highlighted with a black border.
        """
        self.draw_text(screen, "Username:", 50, 50)
        pygame.draw.rect(screen, BLACK if self.active_input ==
                         "username" else WHITE, (50, 85, 310, 30), 2)
        self.draw_text(screen, self.username, 55, 90)

        self.draw_text(screen, "Room Number:", 50, 150)
        pygame.draw.rect(screen, BLACK if self.active_input ==
                         "room_number" else WHITE, (50, 185, 64, 30), 2)
        self.draw_text(screen, self.room_number, 55, 190)
        self.draw_button(screen, "Conect", 250, 230, 90, 35)

    def get_state(self):
        """
        Returns the current state of the login logic.

        Returns:
        - tuple: A tuple containing the username, room_number, and active_input.
        """
        return self.username, self.room_number, self.active_input

    def get_logged(self):
        """
        Returns the player's identifier.

        Returns:
        - int: The player's identifier.
        """

        return self.me
