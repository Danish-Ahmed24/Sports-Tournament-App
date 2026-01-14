from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Manager)
admin.site.register(Referee)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Invitation)
