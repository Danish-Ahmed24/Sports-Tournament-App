import time
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import Error
from django.views.decorators.http import require_http_methods
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from tournament.models import CustomUser, Invitation, Manager, Player, Referee, Team
from .forms import BasicSignUpForm, InvitationForm, TeamSignUpForm, PlayerSignUpForm
from django.utils import timezone


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
    
    invitations = request.user.customUser.manager.sent_invitations.all()
    context={"invitations":invitations}
    return render(request, "tournament/manager/dashboard.html",context)

@login_required
def player_dashboard(request):
    """Player's dashboard"""
    if request.user.customUser.role != "PLAYER":
        return redirect('index')
    
    invitations = request.user.customUser.player.received_invitations.filter(status='P')
    context={"invitations":invitations}
    return render(request, "tournament/player/dashboard.html",context)

@login_required
def referee_dashboard(request):
    """Referee's dashboard"""
    if request.user.customUser.role != "REFEREE":
        return redirect('index')
    return render(request, "tournament/referee/dashboard.html")

@require_http_methods(['POST','GET'])
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
@require_http_methods(['GET'])
def view_available_players(request):
    available_players = Player.objects.filter(isAvailable = True)
    
    if request.user.customUser.role == "MANAGER":
            manager = request.user.customUser.manager
            for player in available_players:
                player.has_invited = player.received_invitations.filter(
                    manager=manager,
                    status='P'  # Only check for PENDING invitations
                ).exists()

    context={
        "available_players":available_players
    }
    return render(request,'tournament/player/browse.html',context)

@login_required
def player_profile(request,pk):
    try:
        player = Player.objects.get(pk=pk)
        if not player.isAvailable:
            return redirect('index')
        if request.user.customUser.role == "MANAGER":
            if player.isAvailable and player.received_invitations.filter(
                manager = request.user.customUser.manager,
                status = "P" 
            ).exists():
                player.has_invited = True
            else:
                player.has_invited = False
        context={
            "player":player
        }
        return render(request,"tournament/player/profile.html",context)
    except ObjectDoesNotExist:
        return not_found(request,"Player Not Found",f"No player found with id ${pk}")
    
@login_required
def send_invite(request, pk):
    # Check if user is a manager
    if request.user.customUser.role != "MANAGER":
        return redirect('index')
    
    try:
        player = Player.objects.get(pk=pk)
    except Player.DoesNotExist:
        return not_found(request,"Player Not Found",f"No player found with id ${pk}")
    
    # Check if player is available
    if not player.isAvailable:
        return not_found(request,"Player already in a team",f"Come back Later")
    
    manager = request.user.customUser.manager
    team = manager.team
    
    if request.method == "POST":
        form = InvitationForm(request.POST)
        if form.is_valid():
            try:
                Invitation.objects.create(
                    player=player,
                    manager=manager,
                    team=team,
                    salary=form.cleaned_data['salary'],
                    contract_length=form.cleaned_data['contract_length'],
                    message=form.cleaned_data['message']
                )
                # Success! Redirect to player profile or players list
                return redirect('player_profile', pk=pk)
            
            except ValidationError as e:
                # Duplicate invitation error
                return not_found(request,"ERROR",e)
    else:
        form = InvitationForm()
    
    # Show the invitation form
    context = {
        'form': form,
        'player': player
    }
    return render(request, 'tournament/invitation/send.html', context)

@login_required
def reject_invitation(request,pk):
    if request.user.customUser.role != "PLAYER":
        return redirect('index')
    
    try:
        invitation = Invitation.objects.get(pk=pk)

        # Security check
        if invitation.player != request.user.customUser.player:
            return not_found(request,"Invitation Not for You",f"Try again later!")
        # Make sure it's pending
        if invitation.status != 'P':
            return not_found(request,"ERROR",f"Invitation has been responded")
        
        invitation.status='R'
        invitation.responded_at=timezone.now()
        invitation.save()
        return redirect('player_dashboard')
    except Invitation.DoesNotExist:
        return not_found(request,"Not Found",f"Invitation not found")
    
@login_required
def accept_invitation(request, pk):
    if request.user.customUser.role != "PLAYER":
        return redirect('index')
    
    try:
        invitation = Invitation.objects.get(pk=pk)
        
        # Make sure this invitation belongs to the logged-in player
        if invitation.player != request.user.customUser.player:
            return not_found(request,"Invitation not for you",f"Try again later")
        
        # Make sure invitation is still pending
        if invitation.status != 'P':
            return not_found(request,"Already Responded",f"Inviatation is already been reponseded")
        
        player = invitation.player
        
        # Update player
        player.team = invitation.team
        player.isAvailable = False
        player.save()
        
        # Accept this invitation
        invitation.status = 'A'
        invitation.responded_at = timezone.now() 
        invitation.save()
        
        # Reject all other pending invitations for this player
        player.received_invitations.filter(status='P').exclude(pk=pk).update(
            status='R',
            responded_at=timezone.now()
        )
        
        return redirect('player_dashboard')
        
    except Invitation.DoesNotExist:
        return not_found(request,"Not Found",f"Invitation Doesnt Exits")

def not_found(request,title,desc):
    context = {
        "title":title,
        "description": desc
    }
    return render(request,"tournament/auth/notFound.html",context)

@login_required
def remove_player(request,pk):
    
    if request.user.customUser.role != "MANAGER":
        return redirect('index')
    manager = request.user.customUser.manager
    
    try:
        player = Player.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return not_found(request,"Player Not Found",f"No player found with id ${pk}")
    
    if manager != player.team.manager:
        return not_found(request,"Permission Denied",f"It is not your player")

    player.isAvailable = True
    player.team = None
    player.save()
    
    return redirect('manager_dashboard')    
