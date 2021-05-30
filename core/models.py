from django.db import models
from django.core.files.storage import FileSystemStorage

import csv
import random
import os

# FIXME Stärker mit gets arbeiten bei den many-to-many fields

# Draw 6 cards + one card for each player, so everyone can draw a different card
def draw_cards(number = 6, already_selected_cards = []):
    #FIXME check if out of bounds
    card_pool = Card.objects
    for already_selected_card in already_selected_cards:
        #print("Excluded:", already_selected_card)
        card_pool = card_pool.exclude(id=already_selected_card)
        #print("Length of all cards:", len(card_pool.all()))
    return random.sample(list(card_pool.all()), number)

class Card(models.Model):
    line = models.CharField(max_length=200)

class Player(models.Model):
    username = models.CharField(max_length=200)
    points = models.IntegerField(default=0)
    selected_card = models.IntegerField(default = 0)

    def select_card(self, card):
        #FIXME check if out of bounds
        self.selected_card = card
        self.save()

class Game(models.Model):
    players = models.ManyToManyField(Player)
    points_to_win = models.IntegerField(default=10)

    last_winner = models.IntegerField(default=0)

    current_round = models.IntegerField(default=0)
    current_player = models.IntegerField(default=0)
    current_cards = models.ManyToManyField(Card)

    current_image = models.IntegerField(default=0)

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

    def get_judge(self):
        return self.players.all()[self.judge]
    
    def get_last_winner(self):
        return self.players.all()[self.last_winner]

    def get_previous_player(self, current):
        player_number = current - 1
        if 0 <= player_number:
            return player_number
        else:
            return len(self.players.all()) - 1

    # Used in templates
    def get_player_before_current(self):
        return self.get_previous_player(self.current_player)

    def get_last_winner(self):
        return self.players.all()[self.last_winner]

    def init_game(self):
        # FIXME, check if 3 players min, 6 players max

        # Initialize all game variables
        self.current_round = 1
        self.current_player = 0
        self.judge = len(self.players.all()) - 1
        self.current_cards.set(draw_cards())
        for player in self.players.all():
            player.points = 0
            player.save()
            player.select_card(-1)
        self.last_winner = 0
        self.save()
        self.randomly_select_image()

    def select_card(self, position_ID):

        # Assign the card to the player
        selected_card = self.get_current_cards()[position_ID]
        
        # This will also result in the card being displayed in "get_selected_cards()"
        self.get_current_player().select_card(selected_card.id)

        print(self.get_current_player().username, "selected:", selected_card.id)

    def submit_card(self):
        
        # Do different things, based on whether the current player is the judge
        if self.current_player != self.judge:
            
            # Draw new cards
            self.current_cards.set(draw_cards(6, self.get_selected_cards()))
            
            # Move to the next player
            self.move_to_next_player()

            # Display the next player starting screen
            return 'next_player_start'

        else:

            # Choose the winning card
            game_was_won = self.choose_winning_card()

            # Display the score overview either as game being won completely or only for one round
            if game_was_won:
                return 'game_was_won'
            else:
                return 'score_overview'

        self.save()

    def get_selected_cards(self, numeric = True):
        cards = []

        for i, player in enumerate(self.players.all()):
            if i != self.judge:
                # FIXME Check if in bounds
                query = Card.objects.filter(id=player.selected_card)
                if len(query) > 0:
                    if numeric:
                        cards.append(query[0].id)
                    else:
                        cards.append(query[0])

        return cards

    def move_to_next_player(self):
        self.current_player = self.get_next_player(self.current_player)
        self.save()

    def choose_winning_card(self):

        card_selected_by_judge = self.get_judge().selected_card
        print("The card selected by the judge is:", card_selected_by_judge)

        for i, player in enumerate(self.players.all()):
            print(player.username, "turned in:", player.selected_card)
            if i != self.judge:
                if card_selected_by_judge == player.selected_card:
                    self.last_winner = i
                    self.save()
                    player.points += 1
                    player.save()

        print("The winner is:", self.get_last_winner().username)            
        
        # Check if the game has been won
        if self.get_last_winner().points >= self.points_to_win:
            return True

        return False

    def get_last_winning_line(self):
        # FIXME Check in bounds
        return Card.objects.filter(id=self.get_last_winner().selected_card)[0].line

    def get_current_cards(self):
        if self.current_player == self.judge:
            return self.get_selected_cards(numeric=False)
        else:
            return self.current_cards.all()

    def move_to_next_round(self):
        # Set the new judge to be the player before the current player
        self.judge = self.get_previous_player(self.judge)
        self.current_round += 1
        self.current_cards.set(draw_cards())
        for player in self.players.all():
            player.select_card(-1)
        self.randomly_select_image()
        self.save()

    def randomly_select_image(self):
        fs = FileSystemStorage(location='core/media/memes/PNG')
        self.current_image = random.randint(0, len(fs.listdir("")[1]))
        self.save()

    def get_current_image(self):
        fs = FileSystemStorage(location='core/media/memes/PNG')
        return os.path.join('/media/core/media/memes/PNG/', fs.listdir("")[1][self.current_image])
