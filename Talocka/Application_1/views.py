from django.shortcuts import render
from django.shortcuts import render, redirect
from datetime import datetime
# from .forms import ConnexionForm,InscriptionForm
from .forms import ProjetForm
from .models import Projet_User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

@login_required
def accueil(request):
    return render(request, "accueil.html")

def projets(request):
    form = ProjetForm()
    return render(request,'projets.html',{"form":form})

@login_required
def create_projet(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = form.save(commit=False) 
            projet.utilisateur = request.user 
            projet.date_de_creation = datetime.now().date()
            projet.date_de_modification = datetime.now().date()
            projet.save()  

            return redirect('projets')  

    else:
        form = ProjetForm()  

    return render(request, 'projets.html', {'form': form})