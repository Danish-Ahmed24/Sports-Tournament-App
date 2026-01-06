from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

ROLE_CHOICES = [
    ("PLAYER", "Player"),
    ("MANAGER", "Manager"),
    ("REFEREE", "Referee"),
]

PLAYER_POSITIONS = [
    ("ST", "Striker"),
    ("LW", "Left Wing"),
    ("RW", "Right Wing"),
    ("CAM", "Center Attack Mid"),
    ("CDM", "Center Defence Mid"),
    ("CM", "Center Mid"),
    ("LM", "Left Mid"),
    ("RM", "Right Mid"),
    ("CB", "Center Back"),
    ("LB", "Left Back"),
    ("RB", "Right Back"),
    ("GK", "Goal Keeper"),
]

class CustomUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="PLAYER")
    name = models.CharField(max_length=100)
    experience = models.IntegerField(validators=[MinValueValidator(0)])

class Player(models.Model):
    customUser = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    position = models.CharField(max_length=10, choices=PLAYER_POSITIONS)
    age = models.IntegerField(validators=[MinValueValidator(18)])

class Manager(models.Model):
    customUser = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    teamName = models.CharField(max_length=30)

class Referee(models.Model):
    customUser = models.OneToOneField(CustomUser, on_delete=models.CASCADE)