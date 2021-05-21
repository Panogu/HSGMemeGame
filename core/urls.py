from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('add_user/', views.add_user, name='add_user'),
    path('start/', views.start, name='start'),
    path('round/', views.current_round, name='round'),
    path('next/', views.next_player, name='next'),
    path('select_card/<int:ID>', views.select_card, name='select_card')
]