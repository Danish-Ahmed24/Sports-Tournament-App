from django.conf import settings
from django.db import models
from django.forms import IntegerField
from django.core.validators import MinValueValidator

roleChoices = {
    "PLAYER": "Player",
    "MANAGER":"Manager",
    "REFREE": "Refree"
}

class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(choices=roleChoices,default="PLAYER")
    experience = models.IntegerField(validators=[MinValueValidator(0)])