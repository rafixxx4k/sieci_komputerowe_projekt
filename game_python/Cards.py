import pygame
import os


class Cards:
    """
    A class representing a deck of cards in a game.

    Attributes:
    - deck: A list representing the cards in the deck.
    - deck_sprite: A list representing the sprites of the cards in the deck.
    - totem: An image representing the totem card.
    - totem_sprite: A sprite representing the totem card.
    """

    def __init__(self):
        self.deck = []
        self.deck_sprite = []

    def image_load(self):
        """
        Loads the images for the game and initializes the sprite objects.

        This method loads the card images and the totem image from the "img" directory.
        It creates sprite objects for each card image and the totem image, and stores them in the respective lists.

        Args:
            self: The GameLogic object.

        Returns:
            None
        """
        for i in range(1, 5):
            for x in ["c", "f", "n", "p", "z"]:
                file_path = os.path.join("./../img", f"{i}{x}.png")
                texture = pygame.image.load(file_path)
                self.deck.append(texture)

        file_path = os.path.join("./../img", "totem.png")
        self.totem = pygame.image.load(file_path)

        file_path = os.path.join("./../img", "disconnected.png")
        self.disconnected = pygame.image.load(file_path)

        for texture in self.deck:
            sprite = pygame.sprite.Sprite()
            sprite.image = texture
            sprite.rect = sprite.image.get_rect()
            self.deck_sprite.append(sprite)

        self.totem_sprite = pygame.sprite.Sprite()
        self.totem_sprite.image = self.totem
        self.totem_sprite.rect = sprite.image.get_rect()

        self.disconnected_sprite = pygame.sprite.Sprite()
        self.disconnected_sprite.image = self.disconnected
        self.disconnected_sprite.rect = sprite.image.get_rect()
