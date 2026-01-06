from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from tournament.models import CustomUser, Manager, Player, Referee
from .forms import BasicSignUpForm, ManagerSignUpForm, PlayerSignUpForm

@login_required
def index(request):
    return render(request,"tournament/index.html")

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
                return redirect('details_manager')
            else:
                #referee
                Referee.objects.create(customUser = customUser)
                return redirect("index")
              
    else:
        form = BasicSignUpForm()

    return render(request, 'tournament/signup.html', {"form": form,"btn":"Next"})


def details_manager(request):
    if 'customUser_pk' not in request.session:
        return redirect('signup')
    if request.method == "POST":
        form = ManagerSignUpForm(request.POST)
        if form.is_valid():
            teamName = form.cleaned_data['teamName']
            customUser = CustomUser.objects.get(pk=request.session['customUser_pk'])
            Manager.objects.create(teamName=teamName,customUser=customUser)
            del request.session['customUser_pk']
            return redirect('index')
    else:
        form = ManagerSignUpForm()
    
    return render(request,"tournament/signup.html",{"form":form,"btn":"Done"})

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

    return render(request,"tournament/signup.html",{"form":form,"btn":"Done"})