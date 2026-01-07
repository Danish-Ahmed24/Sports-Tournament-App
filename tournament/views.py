from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from tournament.models import CustomUser, Manager, Player, Referee, Team
from .forms import BasicSignUpForm, TeamSignUpForm, PlayerSignUpForm

def index(request):
    """Homepage - shows landing page or redirects to dashboard"""
    if request.user.is_authenticated:
        role = request.user.customUser.role
        if role == "PLAYER":
            return redirect('player_dashboard')
        elif role == "MANAGER":
            return redirect('manager_dashboard')
        else:
            return redirect('referee_dashboard')
    
    # Show landing page for guests
    return render(request, "tournament/index.html")

@login_required
def manager_dashboard(request):
    """Manager's dashboard"""
    if request.user.customUser.role != "MANAGER":
        return redirect('index')
    return render(request, "tournament/manager/dashboard.html")

@login_required
def player_dashboard(request):
    """Player's dashboard"""
    if request.user.customUser.role != "PLAYER":
        return redirect('index')
    return render(request, "tournament/player/dashboard.html")

@login_required
def referee_dashboard(request):
    """Referee's dashboard"""
    if request.user.customUser.role != "REFEREE":
        return redirect('index')
    return render(request, "tournament/referee/dashboard.html")

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = BasicSignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            role = form.cleaned_data['role']
            customUser = CustomUser.objects.create(
                user=user,
                role=role,
                experience=form.cleaned_data['experience'],
                name = form.cleaned_data['name']
            )
            login(request, user)
            request.session['customUser_pk'] = customUser.pk
            if(role == "PLAYER"):
                return redirect('details_player')
            elif(role == "MANAGER"):
                return redirect('details_team')
            else:
                #referee
                Referee.objects.create(customUser = customUser)
                del request.session['customUser_pk']
                return redirect("index")
              
    else:
        form = BasicSignUpForm()

    return render(request, 'tournament/auth/signup.html', {"form": form,"btn":"Next"})


def details_team(request):
    if 'customUser_pk' not in request.session:
        return redirect('signup')
    if request.method == "POST":
        form = TeamSignUpForm(request.POST)
        if form.is_valid():
            teamName = form.cleaned_data['teamName']
            customUser = CustomUser.objects.get(pk=request.session['customUser_pk'])
            manager = Manager.objects.create(customUser=customUser)
            Team.objects.create(teamName=teamName,manager=manager)
            del request.session['customUser_pk']
            return redirect('index')
    else:
        form = TeamSignUpForm()
    
    return render(request,"tournament/auth/signup.html",{"form":form,"btn":"Done"})

def details_player(request):
    if 'customUser_pk' not in request.session:
        return redirect('signup')
    if request.method=="POST":
        form = PlayerSignUpForm(request.POST)
        if form.is_valid():
            position = form.cleaned_data['position']
            age = form.cleaned_data['age']
            customUser = CustomUser.objects.get(pk=request.session['customUser_pk'])
            Player.objects.create(position=position,age=age,customUser=customUser)
            del request.session['customUser_pk']
            return redirect('index')
    else:
        form = PlayerSignUpForm()

    return render(request,"tournament/auth/signup.html",{"form":form,"btn":"Done"})

@login_required
def view_available_players(request):
    available_players = Player.objects.filter(isAvailable = True)

    context={
        "available_players":available_players
    }
    return render(request,'tournament/player/browse.html',context)


def player_profile(request,pk):
    try:
        player = Player.objects.get(pk=pk)
        if not player.isAvailable:
            return redirect('index')
        context={
            "player":player
        }
        return render(request,"tournament/player/profile.html",context)
    except ObjectDoesNotExist:
        return HttpResponse("DOes not exits go back")