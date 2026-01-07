from django.urls import include, path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
# app_name = 'tournament'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',LoginView.as_view(template_name="tournament/login.html"),name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('signup/',views.signup_view,name='signup'),
    path('details/player/',views.details_player,name="details_player"),
    path('details/team/',views.details_team,name="details_team"),
    path('players/',views.view_available_players,name='view_available_players'),
    path('player/<int:pk>/',views.player_profile,name="player_profile")
] 