import threading
from threading import Semaphore
from Player import Player
from GameState import GameState
from Cards import Cards
from constants import WINDOW_WIDTH, FONT_SIZE_SMALL, BLACK, UPDATE_SEMAPHORE
import pygame
import os
import socket


class GameLogic:
    """
    Represents the game logic for the multiplayer game.

    Attributes:
        positions (list): A list of dictionaries representing the positions of the game objects.
        board_type (list): A list of lists representing the board type.
    """

    positions = [
        {"image": (50, 50)},
        {"image": (50, 200)},
        {"image": (50, 350)},
        {"image": (WINDOW_WIDTH - 150, 50)},
        {"image": (WINDOW_WIDTH - 150, 200)},
        {"image": (WINDOW_WIDTH - 150, 350)},
        {"image": (350, 450)},
    ]
    board_type = [
        [],
        [6],
        [6, 1],
        [6, 4, 1],
        [6, 0, 1, 2],
        [6, 4, 3, 0, 1],
        [6, 4, 3, 0, 1, 2],
        [6, 5, 4, 3, 0, 1, 2],
    ]

    def __init__(self, me, client_socket: socket.socket):
        """
        Initializes a new instance of the GameLogic class.

        Args:
            me (int): The player's identifier.
            client_socket (socket): The client socket for communication with the server.
        """
        self.me = me
        self.client_socket = client_socket
        self.cards = Cards()
        self.cards.image_load()
        self.font = pygame.font.Font(None, FONT_SIZE_SMALL)
        rec = self.client_socket.recv(1024)
        self.make_game_state(rec.decode())
        self.listen_thread = threading.Thread(target=self.listen_for_updates)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def listen_for_updates(self):
        """
        Listens for updates from the server and updates the game state accordingly.
        """
        try:
            while True:
                # Listen for data from the server
                data = self.client_socket.recv(1024)
                if not data:
                    break
                # Acquire the semaphore to update the game state
                UPDATE_SEMAPHORE.acquire()
                # Update the game state
                self.make_game_state(data.decode())
                # Release the semaphore to signal the main thread
                UPDATE_SEMAPHORE.release()

        except Exception as e:
            print(f"Error in listen_for_updates: {e}")

    def make_game_state(self, state):
        """
        Parses the game state received from the server and updates the game state.

        Args:
            state (str): The game state received from the server.
        """
        state = state.replace("\x00", "")
        winner = int(state[0])
        number_of_players = int(state[1])
        who_to_move = int(state[2])
        message = int(state[3])
        self.gameState = GameState(
            winner,
            number_of_players,
            who_to_move,
            message,
            [Player() for _ in range(number_of_players)],
        )
        for i in range(number_of_players):
            index = 4 + i * 20
            self.gameState.players[i].name = state[index : index + 14]
            self.gameState.players[i].cards_on_hand = int(
                state[index + 14 : index + 16]
            )
            self.gameState.players[i].cards_on_table = int(
                state[index + 16 : index + 18]
            )
            self.gameState.players[i].card_face_up = int(state[index + 18 : index + 20])

    def mouse_handler(self, event):
        """
        Handles the mouse events and updates the game state accordingly.

        Args:
            event (pygame.event.Event): The mouse event.
        """
        # Acquire the semaphore before updating the game state
        UPDATE_SEMAPHORE.acquire()
        if 200 <= event.pos[0] <= 600 and 50 <= event.pos[1] < 400:
            self.client_socket.send("t".encode())
        elif 200 <= event.pos[0] <= 600 and 400 <= event.pos[1] < 600:
            if self.gameState.who_to_move == self.me:
                self.client_socket.send("c".encode())
            else:
                print("it is not your turn")
        # Release the semaphore after updating the game state
        UPDATE_SEMAPHORE.release()

    def draw_text(self, surface, text, x, y):
        """
        Draws text on the given surface at the specified position.

        Args:
            surface (pygame.Surface): The surface to draw on.
            text (str): The text to draw.
            x (int): The x-coordinate of the position.
            y (int): The y-coordinate of the position.
        """
        text_surface = self.font.render(text, True, BLACK)
        surface.blit(text_surface, (x, y))

    def draw_game_seen(self, screen):
        """
        Draws the game state on the screen.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
        """
        # Acquire the semaphore before updating the game state
        UPDATE_SEMAPHORE.acquire()
        # draw totem
        sprite = self.cards.totem_sprite
        sprite.rect.topleft = (300, 100)
        screen.blit(sprite.image, sprite.rect)
        # draw players and cards
        for i, j in enumerate(self.board_type[self.gameState.number_of_players]):
            person = (self.me - 1 + i) % self.gameState.number_of_players

            persons_name = self.gameState.players[person].name
            persons_hand = self.gameState.players[person].cards_on_hand
            persons_table = self.gameState.players[person].cards_on_table
            persons_up = self.gameState.players[person].card_face_up

            if persons_up == -1:
                sprite = self.cards.disconnected_sprite
            else:
                sprite = self.cards.deck_sprite[persons_up]

            x, y = self.positions[j]["image"]
            self.draw_text(
                screen,
                f"{persons_name}: {persons_hand}/{persons_table}",
                x - 30,
                y + 108,
            )
            sprite.rect.topleft = (x, y)
            screen.blit(sprite.image, sprite.rect)
        # if player is to move draw green frame around his cards
        if self.gameState.who_to_move == self.me:
            pygame.draw.rect(screen, (0, 255, 0), (300, 400, 200, 200), 5)
        # else draw yellow frame around person to move
        else:
            position = (
                self.gameState.who_to_move - self.me + self.gameState.number_of_players
            ) % self.gameState.number_of_players
            x, y = self.positions[
                self.board_type[self.gameState.number_of_players][position]
            ]["image"]
            x, y = x - 50, y - 50
            pygame.draw.rect(screen, (255, 255, 0), (x, y, 200, 200), 5)

        # Release the semaphore after updating the game state
        UPDATE_SEMAPHORE.release()
