from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from tournament.models import Player
from .forms import SignUpForm

@login_required
def index(request):
    return render(request,"tournament\index.html")

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            Player.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                experience=form.cleaned_data['experience']
            )
            login(request, user)
            return redirect('role_based_attr')  
    else:
        form = SignUpForm()

    return render(request, 'tournament/signup.html', {"form": form})


