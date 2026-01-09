import time
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import Error
from django.forms import ValidationError
from django.http import HttpResponse
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

def helper_addHasInvitedAttr(request, available_players):
    if request.user.customUser.role == "MANAGER":
        manager = request.user.customUser.manager
        for player in available_players:
            player.has_invited = player.received_invitations.filter(
                manager=manager,
                status='P'  # Only check for PENDING invitations
            ).exists()

@login_required
def view_available_players(request):
    available_players = Player.objects.filter(isAvailable = True)
    helper_addHasInvitedAttr(request,available_players)

    context={
        "available_players":available_players
    }
    return render(request,'tournament/player/browse.html',context)


def player_profile(request,pk):
    try:
        player = Player.objects.get(pk=pk)
        if not player.isAvailable:
            return redirect('index')
        if request.user.customUser.role == "MANAGER":
            if player.isAvailable and player.received_invitations.filter(
                manager = request.user.customUser.manager,
                status = "P" 
            ):
                player.has_invited = True
            else:
                player.has_invited = False
        context={
            "player":player
        }
        return render(request,"tournament/player/profile.html",context)
    except ObjectDoesNotExist:
        return HttpResponse("DOes not exits go back")
    
@login_required
def send_invite(request, pk):
    # Check if user is a manager
    if request.user.customUser.role != "MANAGER":
        return redirect('index')
    
    try:
        player = Player.objects.get(pk=pk)
    except Player.DoesNotExist:
        return HttpResponse("Player not found")
    
    # Check if player is available
    if not player.isAvailable:
        return HttpResponse("Player is already signed to a team")
    
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
                return HttpResponse(f"Error: {e}")
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
            return HttpResponse("This invitation is not for you!")
        # Make sure it's pending
        if invitation.status != 'P':
            return HttpResponse("This invitation has already been responded to")
        
        invitation.status='R'
        invitation.responded_at=timezone.now()
        invitation.save()
        return redirect('player_dashboard')
    except Invitation.DoesNotExist:
        return HttpResponse("Invitation does not exist")
    
@login_required
def accept_invitation(request, pk):
    if request.user.customUser.role != "PLAYER":
        return redirect('index')
    
    try:
        invitation = Invitation.objects.get(pk=pk)
        
        # Make sure this invitation belongs to the logged-in player
        if invitation.player != request.user.customUser.player:
            return HttpResponse("This invitation is not for you!")
        
        # Make sure invitation is still pending
        if invitation.status != 'P':
            return HttpResponse("This invitation has already been responded to")
        
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
        return HttpResponse("Invitation does not exist")

