from django.urls import include, path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
# app_name = 'tournament'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name="tournament/auth/login.html"), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('details/player/', views.details_player, name="details_player"),
    path('details/team/', views.details_team, name="details_team"),

    # Dashboards
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('player/dashboard/', views.player_dashboard, name='player_dashboard'),
    path('referee/dashboard/', views.referee_dashboard, name='referee_dashboard'),
    
    # Other pages
    path('browse/players/', views.view_available_players, name='view-available-players'),
    path('player/<int:pk>/', views.player_profile, name="player_profile"),

    # Invitations
    path('player/<int:pk>/invite',views.send_invite,name="send_invite"),
    path('accept_invitation/<int:pk>/',views.accept_invitation,name="accept_invitation"),
    path('reject_invitation/<int:pk>/',views.reject_invitation,name="reject_invitation"),

    # Remove
    path('player/<int:pk>/close',views.remove_player,name="remove_player"),

]