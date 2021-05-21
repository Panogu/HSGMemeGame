from django.shortcuts import render
from django.http import HttpResponse

from .models import Game, Player, Card

# TODO get game by ID (Hash)
def get_current_game_or_create_it():
    # Create the dummy cards
    if (len(Card.objects.all()) < 12):
        for i in range(1, 13):
            card = Card(line="Dummy Line " + str(i))
            card.save()

    # Create a single game
    current_game = Game()
    if (len(Game.objects.all()) == 0):
        current_game.save()
    else:
        current_game = Game.objects.all()[0]
    return current_game

# The index function, which is called, when the game's domain is requested
def index(request):
    current_game = get_current_game_or_create_it()    

    context = {'current_game': current_game}
    return render(request, 'core/index.html', context)

def add_user(request):
    current_game = get_current_game_or_create_it()
    
    username = request.POST.get('username', "")
    
    if (username != ""):
        player = Player(username=username)
        player.save()
        current_game.players.add(player)
    
    context = {'current_game': current_game}
    
    return render(request, 'core/index.html', context)

def start(request):
    current_game = get_current_game_or_create_it()

    current_game.init_game()

    # TODO make more beautiful - in model
    current_player = current_game.players.all()[current_game.current_player]

    context = {'current_game': current_game, 'current_player': current_player}

    return render(request, 'core/round_start.html', context)

def current_round(request):
    current_game = get_current_game_or_create_it()

    current_player = current_game.players.all()[current_game.current_player]

    context = {'current_game': current_game, 'current_player': current_player}

    return render(request, 'core/round_main.html', context)

def select_card(request, ID):
    current_game = get_current_game_or_create_it()
    current_game.assign_card_to_player(ID)

    current_player = current_game.players.all()[current_game.current_player]

    context = {'current_game': current_game, 'current_player': current_player, 'current_card': ID}

    return render(request, 'core/round_main.html', context)

# Next Player
# FIXME Merge with startup?
def next_player(request):
    current_game = get_current_game_or_create_it()

    current_game.move_to_next_player()
    
    current_player = current_game.players.all()[current_game.current_player]

    context = {'current_game': current_game, 'current_player': current_player}

    return render(request, 'core/round_start.html', context)

    