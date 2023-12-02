import pygame
import socket
from constants import WHITE, DARK_GRAY, BLACK, FONT_SIZE


class LoginLogic:
    def __init__(self):
        self.logged = False
        self.username = ""
        self.room_number = ""
        self.active_input = "username"
        self.font = pygame.font.Font(None, FONT_SIZE)

    def send_credential(self):
        if len(self.username) > 0 and len(self.room_number) == 4:
            print(f'user: {self.username}, room: {self.room_number}')
            try:
                client_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(('localhost', 1100))
                message = f"{self.room_number:04}{self.username:<14}"
                client_socket.send(message.encode())
                print(client_socket.recv(1024))
                client_socket.close()
                self.logged = True
                print("Dane wysłane do serwera.")
            except Exception as e:
                print(f"Błąd podczas połączenia z serwerem: {e}")
        else:
            print("Niepoprawne dane. Wprowadź poprawne dane.")

    def keyboard_handler(self, event):
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
        if 50 <= event.pos[0] <= 350 and 50 <= event.pos[1] < 150:
            return "username"
        elif 50 <= event.pos[0] <= 350 and 150 <= event.pos[1] < 230:
            return "room_number"
        elif 250 <= event.pos[0] <= 340 and 230 <= event.pos[1] <= 265:
            self.send_credential()
        return self.active_input

    def draw_text(self, surface, text, x, y):

        text_surface = self.font.render(text, True, BLACK)
        surface.blit(text_surface, (x, y))

    # Funkcja rysująca przycisk

    def draw_button(self, surface, text, x, y, width, height):
        pygame.draw.rect(surface, DARK_GRAY, (x, y, width, height), 0, 5)
        pygame.draw.rect(surface, BLACK, (x, y, width, height), 2, 5)
        self.draw_text(surface, text, x+6, y+6)

    # Funkcja rysująca ekran logowania

    def draw_login_screen(self, screen):
        # Rysowanie pól tekstowych
        self.draw_text(screen, "Username:", 50, 50)
        pygame.draw.rect(screen, BLACK if self.active_input ==
                         "username" else WHITE, (50, 85, 310, 30), 2)
        self.draw_text(screen, self.username, 55, 90)

        self.draw_text(screen, "Room Number:", 50, 150)
        pygame.draw.rect(screen, BLACK if self.active_input ==
                         "room_number" else WHITE, (50, 185, 64, 30), 2)
        self.draw_text(screen, self.room_number, 55, 190)
        # Rysowanie przycisku "Dołącz"
        self.draw_button(screen, "Dołącz", 250, 230, 90, 35)

    def get_state(self):
        return self.username, self.room_number, self.active_input

    def get_logged(self):
        return self.logged
