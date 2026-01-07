from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="customUser")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="PLAYER")
    name = models.CharField(max_length=100)
    experience = models.IntegerField(validators=[MinValueValidator(0)])

    def save(self,*args, **kwargs):
        if self.pk:
            original = CustomUser.objects.get(pk=self.pk)
            if original.role != self.role:
                raise ValidationError("Role cannot be changed once assigned")
        super().save(*args, **kwargs)

class Manager(models.Model):
    customUser = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="manager")

class Referee(models.Model):
    customUser = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="referee")

class Team(models.Model):
    teamName = models.CharField(max_length=50,unique=True)
    manager=models.OneToOneField(Manager, on_delete=models.CASCADE,related_name="team")

    # players , manager
    
class Player(models.Model):
    customUser = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name="player")
    position = models.CharField(max_length=10, choices=PLAYER_POSITIONS)
    age = models.IntegerField(validators=[MinValueValidator(18)])
    # abi form and view mein change nhi kia hai mene 
    # bool suppose kia hai not string 
    # [("AVAILABLE","Free Agent"),("SIGNED","on a team")]
    isAvailable = models.BooleanField(default=True) 
    team = models.ForeignKey(Team, on_delete=models.SET_NULL,related_name="players",blank=True,null=True)


