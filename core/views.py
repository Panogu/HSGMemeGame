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
    current_game.init_game()  

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

def add_user(request):

    current_game = get_current_game_or_create_it()
    
    username = request.POST.get('username', "")
    print("New user:", username)
    
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

def display_cards_to_chose_from(request):
    current_game = get_current_game_or_create_it()

    # FIXME own function
    context = {'current_game': current_game, 'current_player': current_game.get_current_player(), 'current_cards': current_game.get_current_player().get_cards()}
    return render(request, 'core/round_main.html', context)

def select_card(request, ID):
    current_game = get_current_game_or_create_it()
    current_game.assign_card_to_player(ID)

    current_player = current_game.players.all()[current_game.current_player]

    # FIXME own function
    context = {'current_game': current_game, 'current_player': current_game.get_current_player(), 'current_cards': current_game.get_current_player().get_cards(), 'current_card': ID}
    return render(request, 'core/round_main.html', context)

def submit_card(request):
    current_game = get_current_game_or_create_it()
    current_player = current_game.get_current_player()
    print("Player:", current_game.current_player)
    print("Judge:", current_game.judge)
    # Check if current player is judge
    if current_game.current_player == current_game.judge:
        current_game.judge_evaluation()
        current_game.move_to_next_round()

        context = {'current_game': current_game}
        return render(request, 'core/results.html', context)
    else:
        current_game.move_to_next_player()

        context = {'current_game': current_game, 'current_player': current_game.get_current_player(), 'current_cards': current_game.get_current_player().get_cards()}
        return render(request, 'core/round_start.html', context)

def results(request):
    context = {'current_game': current_game}
    return render(request, 'core/results.html', context)

def next_round(self):
    context = {'current_game': current_game, 'current_player': current_game.get_current_player(), 'current_cards': current_game.get_current_player().get_cards()}
    return render(request, 'core/round_start.html', context)

    