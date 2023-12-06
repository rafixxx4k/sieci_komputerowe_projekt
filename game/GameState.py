from Player import Player


class GameState:
    """
    Represents the state of the game.

    Attributes:
        winner (str): The winner of the game.
        number_of_players (int): The number of players in the game.
        who_to_move (str): The player who is currently making a move.
        message (str): A message to display to the players.
        players (list): A list of Player objects representing the players in the game.
    """

    def __init__(self, winner, number_of_players, who_to_move, message, players):
        self.winner = winner
        self.number_of_players = number_of_players
        self.who_to_move = who_to_move
        self.message = message
        self.players = players
