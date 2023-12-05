import socket
import threading
import time
import random

# Dictionary to store game state for each room
game_rooms = {}
NUMBER_OF_CARDS = 19


class Player:
    def __init__(self, name='', cards_on_hand=0, cards_on_table=0, card_face_up=0, socket=None):
        self.name = name
        self.cards_on_hand = cards_on_hand
        self.cards_on_table = cards_on_table
        self.card_face_up = card_face_up
        self.socket = socket


class GameState:
    def __init__(self, winner, number_of_players, who_to_move, message, list_of_players):
        self.winner = winner
        self.number_of_players = number_of_players
        self.who_to_move = who_to_move
        self.message = message
        self.players = list_of_players


def new_card(game_state, player_number):
    game_state.players[player_number-1].cards_on_hand -= 1
    game_state.players[player_number-1].cards_on_table += 1
    game_state.players[player_number-1].card_face_up = random.randint(
        0, NUMBER_OF_CARDS)
    game_state.who_to_move = (game_state.who_to_move %
                              game_state.number_of_players)+1
    broadcast_game_state(game_state)


def take_totem(game_state, player_number):
    who_to_take = []
    cards_of_player = game_state.players[player_number-1].cards_on_table
    for i, player in enumerate(game_state.players):
        if i == player_number-1:
            continue
        if player.card_face_up//5 == game_state.players[player_number-1].card_face_up//5:
            who_to_take.append(i)
    if len(who_to_take) == 0:
        all_cards_on_table = sum(
            player.cards_on_table for player in game_state.players)
        game_state.players[player_number -
                           1].cards_on_hand += all_cards_on_table-1
        game_state.players[player_number-1].cards_on_table = 1
        game_state.players[player_number-1].card_face_up = random.randint(
            0, NUMBER_OF_CARDS)
        game_state.who_to_move = (
            game_state.who_to_move + 1) % game_state.number_of_players
        for i, player in enumerate(game_state.players):
            if i == player_number-1:
                continue
            player.cards_on_table = 1
            player.card_face_up = random.randint(0, NUMBER_OF_CARDS)
            player.cards_on_hand -= 1
    else:
        game_state.players[player_number-1].cards_on_table = 1
        game_state.players[player_number-1].cards_on_hand -= 1
        game_state.players[player_number-1].card_face_up = random.randint(
            0, NUMBER_OF_CARDS)
        for i in who_to_take:
            game_state.players[i].cards_on_hand += game_state.players[i].cards_on_table + \
                (cards_of_player//len(who_to_take)) - 1
            game_state.players[i].cards_on_table = 1
            game_state.players[i].card_face_up = random.randint(
                0, NUMBER_OF_CARDS)
    broadcast_game_state(game_state)


def handle_client(client_socket):
    try:
        # Receive data from the client
        data = client_socket.recv(32)
        if not data:
            return

        # Handle login
        room_number = int(data[:4].decode().strip())
        player_name = data[4:18].decode().strip()
        player = Player(player_name, 12, 1, random.randint(
            0, NUMBER_OF_CARDS), client_socket)

        # Check if the room exists
        if room_number not in game_rooms:
            game_rooms[room_number] = GameState(0, 0, 1, 0, [])

        # Check if the room is full
        if game_rooms[room_number].number_of_players >= 8:
            client_socket.send('0'.encode())  # Send 0 if room is full
            return

        # Add the player to the room
        game_rooms[room_number].players.append(player)
        game_rooms[room_number].number_of_players += 1

        # Send response to the client with player position
        this_player = game_rooms[room_number].number_of_players
        print(this_player)
        client_socket.send(this_player.to_bytes(1, 'big'))

        # Notify all players in the room about the updated game state
        broadcast_game_state(game_rooms[room_number])

        # Simulate some game updates
        while True:
            data = client_socket.recv(32)
            if not data:
                break
            if data == b'c':
                print("Player clicked")
                new_card(game_rooms[room_number], this_player)
            elif data == b't':
                print("Player took a totem")
                take_totem(game_rooms[room_number], this_player)

        # ... Continue the game logic as needed ...

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


def broadcast_game_state(game_state):
    game_state_bytes = convert_game_state_to_bytes(game_state)
    print(game_state_bytes)
    for player in game_state.players:
        player.socket.send(game_state_bytes)


def convert_game_state_to_bytes(game_state):
    result_byte = f'{game_state.winner}'
    number_of_players_byte = f'{game_state.number_of_players}'
    who_to_move_byte = f'{game_state.who_to_move}'
    message_byte = '0'

    game_state_bytes = result_byte + number_of_players_byte + \
        who_to_move_byte + message_byte

    for player in game_state.players:
        player_name_bytes = f'{player.name:<14}'
        cards_on_hand_bytes = f'{player.cards_on_hand:02}'
        cards_on_table_bytes = f'{player.cards_on_table:02}'
        card_face_up_bytes = f'{player.card_face_up:02}'

        player_bytes = player_name_bytes + cards_on_hand_bytes + \
            cards_on_table_bytes + card_face_up_bytes
        game_state_bytes += player_bytes

    return game_state_bytes.encode()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 1100))
    server.listen(5)
    print("Server listening on port 1100")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        # Start a new thread to handle the client
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()
