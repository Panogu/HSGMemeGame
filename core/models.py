from django.db import models

import random

# FIXME Stärker mit gets arbeiten bei den many-to-many fields

def draw_cards(number=6):
    #FIXME check if out of bounds
    return random.sample(list(Card.objects.all()), number)

class Card(models.Model):
    line = models.CharField(max_length=200)

class Player(models.Model):
    username = models.CharField(max_length=200)
    points = models.IntegerField(default=0)
    selected_cards = models.ManyToManyField(Card)

    def select_card(self, card):
        #FIXME check if out of bounds
        self.selected_cards.set([card])

class Game(models.Model):
    players = models.ManyToManyField(Player)
    points_to_win = models.IntegerField(default=10)

    current_round = models.IntegerField(default=0)
    current_player = models.IntegerField(default=0)

    current_cards = models.ManyToManyField(Card)

    judge = models.IntegerField(default=0)

    # Main Game Logic
    # Return the number of the next player (number of the player + 1 or 0 if again from beginning)
    def get_next_player(self, current):
        player_number = current + 1
        if len(self.players.all()) > player_number:
            return player_number
        else:
            return 0

    def init_game(self):
        # Initialize all game variables
        self.current_round = 1
        self.current_player = 0
        self.judge = len(self.players.all()) - 1
        self.save()

    def assign_card_to_player(self, ID):
        self.players.all()[self.current_player].select_card(self.current_cards.all()[ID])

    def move_to_next_player(self):
        self.current_player = self.get_next_player(self.current_player)
        
        # Choose correct cards: Random for normal player, the cards from the other players for judge
        if self.current_player == self.judge:
            # Display the players' cards
            player_cards = list()
            for player in self.players.all():
                player_cards.extend(list(player.selected_cards.all()))
            self.current_cards.set(player_cards)
        else:
            # Shuffle cards
            self.current_cards.set(draw_cards())

        self.save()

        # Return whether to move to next round
        if self.current_player == self.judge:
            return True
        else:
            return False

    def move_to_next_round(self):
        self.current_round += 1
        self.current_player = self.get_next_player(self.current_player)
        self.judge = self.get_next_player(self.judge)

        self.save()

