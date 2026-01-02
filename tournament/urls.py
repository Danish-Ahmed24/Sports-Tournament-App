from django.urls import path
from . import views

app_name = 'tournament'

urlpatterns = [
    path('', views.home, name='home'),
    # More URLs will be added later
]