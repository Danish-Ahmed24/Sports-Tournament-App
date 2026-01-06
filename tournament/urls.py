from django.urls import include, path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
# app_name = 'tournament'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',LoginView.as_view(template_name="tournament/login.html"),name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('signup/',views.signup_view,name='signup'),
    path('details/player',views.details_player,name="details_player"),
    path('details/manager',views.details_manager,name="details_manager"),
] 