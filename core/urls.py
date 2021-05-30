from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('update_settings/', views.update_settings, name='update_settings'),
    path('remove_user/<int:ID>', views.remove_user, name='remove_user'),
    path('round/', views.display_cards_to_chose_from, name='round'),
    path('select_card/<int:ID>', views.select_card, name='select_card'),
    path('submit_card/', views.submit_card, name='submit_card'),
    path('next_round', views.next_round, name="next_round"),
    path('reload_image', views.reload_image, name="reload_image"),
    path('start', views.start, name="start"),
    path('initial_start', views.initial_start, name="initial_start")
]