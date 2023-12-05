import socket
import threading
import random
from Player import Player
from GameState import GameState

# Dictionary to store game state for each room
game_rooms = {}
NUMBER_OF_CARDS = 19


class GameState:
    def __init__(self, winner, number_of_players, who_to_move, message, list_of_players):
        self.winner = winner
        self.number_of_players = number_of_players
        self.who_to_move = who_to_move
        self.message = message
        self.players = list_of_players


def handle_login(data, client_socket):
    room_number = int(data[:4].decode().strip())
    player_name = data[4:18].decode().strip()
    player = Player(player_name, 12, 1, random.randint(
        0, NUMBER_OF_CARDS), client_socket)
    return room_number, player


def handle_room(room_number, player):
    if room_number not in game_rooms:
        game_rooms[room_number] = GameState(0, 0, 1, 0, [])
    # if room is full sends 0 to client
    if game_rooms[room_number].number_of_players >= 8:
        player.socket.send('0'.encode())
        return False
    game_rooms[room_number].players.append(player)
    game_rooms[room_number].number_of_players += 1
    return True


def handle_client(client_socket):
    """
    Handles the client connection and communication.

    Args:
        client_socket (socket): The client socket object.

    Returns:
        None
    """
    try:
        data = client_socket.recv(32)
        if not data:
            return
        room_number, player = handle_login(data, client_socket)
        if not handle_room(room_number, player):
            return
        # if room is not full sends player id to client
        player_id = game_rooms[room_number].number_of_players
        player.socket.send(str(player_id).encode())
        broadcast_game_state(game_rooms[room_number])
        while True:
            data = client_socket.recv(32)
            if not data:
                return
            if data == b'c':
                new_card(game_rooms[room_number], player)
            elif data == b't':
                take_totem(game_rooms[room_number], player, player_id - 1)
    except Exception as e:
        print(f"Error handling client: {e}")


def broadcast_game_state(game_state):
    game_state_bytes = convert_game_state_to_bytes(game_state)
    print(game_state_bytes)
    for player in game_state.players:
        player.socket.send(game_state_bytes)


def convert_game_state_to_bytes(game_state):
    result_byte = f'{game_state.winner}'
    result_byte += f'{game_state.number_of_players}'
    result_byte += f'{game_state.who_to_move}'
    result_byte += '0'
    for player in game_state.players:
        result_byte += f'{player.name:<14}{player.cards_on_hand:02}{player.cards_on_table:02}{player.card_face_up:02}'
    return result_byte.encode()


def new_card(game_state, player):
    # if there is no card in hand take all cards from table
    if player.cards_on_hand == 0:
        player.cards_on_hand = player.cards_on_table
        player.cards_on_table = 0
    player.cards_on_hand -= 1
    player.cards_on_table += 1
    player.card_face_up = random.randint(0, NUMBER_OF_CARDS)
    game_state.who_to_move = (game_state.who_to_move %
                              game_state.number_of_players) + 1
    broadcast_game_state(game_state)


def take_totem(game_state, player, player_it):
    print(player)
    print(player_it)
    players_with_same_card = [
        p for p in game_state.players if p.card_face_up//5 == player.card_face_up//5]
    if len(players_with_same_card) == 1:
        for p in game_state.players:
            player.cards_on_hand += p.cards_on_table
            p.cards_on_table = 1
            p.cards_on_hand -= 1
            p.card_face_up = random.randint(0, NUMBER_OF_CARDS)
    else:
        numbers_of_cards_after_split = player.cards_on_table//(len(
            players_with_same_card)-1)
        for i, p in enumerate(players_with_same_card):
            if i != player_it:
                p.cards_on_hand += numbers_of_cards_after_split
                p.cards_on_hand += p.cards_on_table
            p.cards_on_table = 1
            p.cards_on_hand -= 1
            p.card_face_up = random.randint(0, NUMBER_OF_CARDS)
    game_state.who_to_move = player_it + 1
    broadcast_game_state(game_state)


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
