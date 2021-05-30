from django.shortcuts import render
from django.http import HttpResponse

from .models import Game, Player, Card

import csv

def create_cards():

    # Load and create the cards
    cards_csv = csv.reader(open('core/media/cards.csv', 'r'))
    data = list(cards_csv)

    if (len(Card.objects.all()) < len(data)):
        Card.objects.all().delete()
        cards_to_create = []
        
        for row in data:
            cards_to_create.append(Card(line=row[0]))

        Card.objects.bulk_create(
            cards_to_create
        )
        

# TODO get game by ID (Hash)
def get_current_game_or_create_it():

    # Create a single game
    current_game = Game()
    if (len(Game.objects.all()) == 0):
        current_game.save()
    else:
        current_game = Game.objects.all()[0]
    return current_game

# The index function, which is called, when the game's domain is requested
def index(request):
    
    create_cards()
    current_game = get_current_game_or_create_it()
    current_game.init_game()

    current_game.randomly_select_image()

    context = {'current_game': current_game}
    return render(request, 'core/index.html', context)

def remove_user(request, ID):
    # TODO check if player is registered
    current_game = get_current_game_or_create_it()
    # FIXME do the TODO by checking the length
    player_to_remove = current_game.players.filter(id=ID)[0]
    current_game.players.remove(player_to_remove)
    context = {'current_game': current_game}
    return render(request, 'core/index.html', context)

def update_settings(request):

    # FIXME ganz andere funktion, nicht createn, sondern zu Startseite verweisen
    current_game = get_current_game_or_create_it()
    
    username = request.POST.get('username', "")
    print("New user:", username)
    
    if (username != ""):
        player = Player(username=username)
        player.save()
        current_game.players.add(player)
    
    points_to_win = request.POST.get('points_to_win', -1)
    if (points_to_win != -1):
        current_game.points_to_win = points_to_win
        current_game.save()

    context = {'current_game': current_game}
    
    return render(request, 'core/index.html', context)

def start(request):
    current_game = get_current_game_or_create_it()
    context = {'current_game': current_game}
    return render(request, 'core/round_start.html', context)

def display_cards_to_chose_from(request):
    current_game = get_current_game_or_create_it()

    # FIXME own function
    context = {'current_game': current_game, 'current_player': current_game.get_current_player(), 'current_cards': current_game.get_current_cards()}
    return render(request, 'core/round_main.html', context)

def select_card(request, ID):
    current_game = get_current_game_or_create_it()
    current_game.select_card(ID)

    # FIXME own function
    context = {'current_game': current_game, 'current_player': current_game.get_current_player(), 'current_cards': current_game.get_current_cards(), 'current_card': ID}
    return render(request, 'core/round_main.html', context)

def submit_card(request):
    current_game = get_current_game_or_create_it()
    current_player = current_game.get_current_player()
    
    next_action = current_game.submit_card()

    if (next_action == 'next_player_start'):
        context = {'current_game': current_game, 'current_player': current_game.get_current_player(), 'current_cards': current_game.get_current_cards()}
        return render(request, 'core/round_start.html', context)
    elif (next_action == 'score_overview'):
        context = {'current_game': current_game}
        return render(request, 'core/results.html', context)
    elif (next_action == 'game_was_won'):
        context = {'current_game': current_game, 'game_was_won': True}
        return render(request, 'core/results.html', context)

def next_round(request):
    current_game = get_current_game_or_create_it()
    current_game.move_to_next_round()

    return start(request)

def reload_image(request):
    current_game = get_current_game_or_create_it()
    current_game.randomly_select_image()
    context = {'current_game': current_game, 'current_player': current_game.get_current_player(), 'current_cards': current_game.get_current_cards()}
    return render(request, 'core/round_start.html', context)

    