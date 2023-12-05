class Player:
    def __init__(self, name='', cards_on_hand=0, cards_on_table=0, card_face_up=0, socket=None):
        """
        Initializes a Player object.

        Args:
            name (str): The name of the player. Defaults to an empty string.
            cards_on_hand (int): The number of cards the player has on hand. Defaults to 0.
            cards_on_table (int): The number of cards the player has on the table. Defaults to 0.
            card_face_up (int): The number of the card that is face up. Defaults to 0.
            socket: The socket object associated with the player. Defaults to None.
        """
        self.name = name
        self.cards_on_hand = cards_on_hand
        self.cards_on_table = cards_on_table
        self.card_face_up = card_face_up
        self.socket = socket
