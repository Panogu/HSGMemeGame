from django.db import models

import random

# FIXME Stärker mit gets arbeiten bei den many-to-many fields

# Draw 6 cards + one card for each player, so everyone can draw a different card
def draw_cards(number_of_players, already_selected_cards = []):
    #FIXME check if out of bounds
    card_pool = Card.objects
    for already_selected_card in already_selected_cards:
        card_pool.exclude(id=already_selected_card.id)
    return random.sample(list(Card.objects.all()), 6+number_of_players)

class Card(models.Model):
    line = models.CharField(max_length=200)

class Player(models.Model):
    username = models.CharField(max_length=200)
    points = models.IntegerField(default=0)
    cards_to_select = models.ManyToManyField(Card)
    selected_card = models.IntegerField(default = 0)

    def select_card(self, card):
        #FIXME check if out of bounds
        self.selected_card = card.id
        self.save()

    def get_cards(self):
        return self.cards_to_select.all()

class Game(models.Model):
    players = models.ManyToManyField(Player)
    points_to_win = models.IntegerField(default=10)

    last_winner = models.IntegerField(default=0)

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

    def get_current_player(self):
        # FIXME Check out of bounds
        return self.players.all()[self.current_player]

    def get_previous_player(self, current):
        player_number = current - 1
        if 0 <= player_number:
            return player_number
        else:
            return len(self.players.all()) - 1

    def get_last_winner(self):
        return self.players.all()[self.last_winner]

    def init_game(self):
        # FIXME, check if 3 players min

        # Initialize all game variables
        self.current_round = 1
        self.current_player = 0
        self.judge = len(self.players.all()) - 1
        self.current_cards.set(draw_cards(len(self.players.all())))
        self.get_current_player().cards_to_select.set(self.get_cards_to_chose_from())
        for player in self.players.all():
            player.points = 0
            player.save()
        self.last_winner = 0
        self.save()

    def get_cards_to_chose_from(self):
        return self.current_cards.all()[0:6]

    def assign_card_to_player(self, ID):
        card_to_assign = self.current_cards.all()[ID]
        self.players.all()[self.current_player].select_card(card_to_assign)
        #self.current_cards.remove(card_to_assign)

    def get_selected_cards(self):
        cards = []

        for i, player in enumerate(self.players.all()):
            if (i != self.judge):
                # FIXME Check if in bounds
                cards.append(Card.objects.filter(id=player.selected_card)[0])

        return cards

    def move_to_next_player(self):
        self.current_player = self.get_next_player(self.current_player)

        # Set the cards of the next player
        if self.current_player != self.judge:
            self.get_current_player().cards_to_select.set(self.get_cards_to_chose_from())
        else:
            self.get_current_player().cards_to_select.set(self.get_selected_cards())
        
        self.save()

    # Calculate the new points and return if the game was won
    def judge_evaluation(self):

        # Get the selected card by the judge
        current_card = self.get_current_player().selected_card

        # Get the corresponding player
        winning_player = None
        print("Winning card: ", current_card)
        for player in self.players.all():
            print("Current card: ", player.selected_card)
            if player.selected_card == current_card and player != self.get_current_player():
                winning_player = player

                # Give the player who chose it one point
                winning_player.points += 1

                # Save the winning player object again
                winning_player.save()

                self.last_winner = player.id
                self.save()

                if winning_player.points >= self.points_to_win:
                    return True

        return False

    def move_to_next_round(self):
        # Set the new judge to be the player before the current player
        self.judge = self.get_previous_player(self.judge)
        self.current_round += 1
        self.current_cards.set(draw_cards(len(self.players.all())))
        self.get_current_player().cards_to_select.set(self.get_cards_to_chose_from())
        self.save()
