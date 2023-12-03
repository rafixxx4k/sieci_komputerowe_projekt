import threading
from threading import Semaphore
from constants import WINDOW_WIDTH, FONT_SIZE_SMALL, BLACK, UPDATE_SEMAPHORE
import pygame
import os
import socket


class Player:
    def __init__(self):
        self.name = ""
        self.cards_on_hand = 0
        self.cards_on_table = 0
        self.card_face_up = 0


class GameState:
    def __init__(self, winner, number_of_players, who_to_move, message):
        self.winner = winner
        self.number_of_players = number_of_players
        self.who_to_move = who_to_move
        self.message = message
        self.players = [Player() for _ in range(number_of_players)]


class Cards:
    def __init__(self):
        self.deck = []
        self.deck_sprite = []

    def image_load(self):
        for i in range(1, 5):
            for x in ["c", "f", "n", "p", "z"]:
                file_path = os.path.join("img", f"{i}{x}.png")
                texture = pygame.image.load(file_path)
                self.deck.append(texture)

        file_path = os.path.join("img", "totem.png")
        self.totem = pygame.image.load(file_path)

        for texture in self.deck:
            sprite = pygame.sprite.Sprite()
            sprite.image = texture
            sprite.rect = sprite.image.get_rect()
            self.deck_sprite.append(sprite)

        self.totem_sprite = pygame.sprite.Sprite()
        self.totem_sprite.image = self.totem
        self.totem_sprite.rect = sprite.image.get_rect()


class GameLogic:
    positions = [
        {"image": (50, 50)},
        {"image": (50, 200)},
        {"image": (50, 350)},
        {"image": (WINDOW_WIDTH-150, 50)},
        {"image": (WINDOW_WIDTH-150, 200)},
        {"image": (WINDOW_WIDTH-150, 350)},
        {"image": (350, 450)}
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

    def __init__(self, me, client_socket):
        self.me = me
        self.client_socket = client_socket
        self.cards = Cards()
        self.cards.image_load()
        self.font = pygame.font.Font(None, FONT_SIZE_SMALL)
        rec = self.client_socket.recv(1024)
        print(rec)
        self.make_game_state(rec.decode())
        self.listen_thread = threading.Thread(target=self.listen_for_updates)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def listen_for_updates(self):
        try:
            while True:
                # Listen for data from the server
                data = self.client_socket.recv(1024)
                if not data:
                    break
                # Acquire the semaphore to update the game state
                UPDATE_SEMAPHORE.acquire()
                # Update the game state
                print("listen for updates semaphore down")
                self.make_game_state(data.decode())
                # Release the semaphore to signal the main thread
                UPDATE_SEMAPHORE.release()

        except Exception as e:
            print(f"Error in listen_for_updates: {e}")

    def make_game_state(self, state):
        winner = int(state[0])
        number_of_players = int(state[1])
        who_to_move = int(state[2])
        message = int(state[3])
        self.gameState = GameState(
            winner, number_of_players, who_to_move, message)
        for i in range(number_of_players):
            index = 4 + i*20
            self.gameState.players[i].name = state[index:index+14]
            self.gameState.players[i].cards_on_hand = int(
                state[index+14:index+16])
            self.gameState.players[i].cards_on_table = int(
                state[index+16:index+18])
            self.gameState.players[i].card_face_up = int(
                state[index+18:index+20])
        for key, value in vars(self.gameState).items():
            print(f"{key}: {value}")

    def mouse_handler(self, event):
        # Acquire the semaphore before updating the game state
        UPDATE_SEMAPHORE.acquire()
        if 200 <= event.pos[0] <= 600 and 50 <= event.pos[1] < 400:
            self.client_socket.send("t".encode())
        elif 200 <= event.pos[0] <= 600 and 400 <= event.pos[1] < 600:
            if self.gameState.who_to_move == self.me:
                self.client_socket.send("c")
            else:
                print("it is not your turn")
        # Release the semaphore after updating the game state
        UPDATE_SEMAPHORE.release()

    def draw_text(self, surface, text, x, y):
        text_surface = self.font.render(text, True, BLACK)
        surface.blit(text_surface, (x, y))

    def draw_game_seen(self, screen):
        # Acquire the semaphore before updating the game state
        UPDATE_SEMAPHORE.acquire()
        # draw totem
        sprite = self.cards.totem_sprite
        sprite.rect.topleft = (300, 100)
        screen.blit(sprite.image, sprite.rect)
        # draw players cards
        for i, j in enumerate(self.board_type[self.gameState.number_of_players]):
            person = (self.me - 1 + i) % self.gameState.number_of_players
            persons_name = self.gameState.players[person].name
            persons_hand = self.gameState.players[person].cards_on_hand
            persons_table = self.gameState.players[person].cards_on_table
            persons_up = self.gameState.players[person].card_face_up
            sprite = self.cards.deck_sprite[persons_up]
            x, y = self.positions[j]["image"]
            self.draw_text(
                screen, f'{persons_name}: {persons_hand}/{persons_table}', x-30, y+108)
            sprite.rect.topleft = (x, y)
            screen.blit(sprite.image, sprite.rect)

        # Release the semaphore after updating the game state
        UPDATE_SEMAPHORE.release()
