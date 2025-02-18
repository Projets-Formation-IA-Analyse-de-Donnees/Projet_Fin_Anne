from django.shortcuts import render
from django.shortcuts import render, redirect
from datetime import datetime
# from .forms import ConnexionForm,InscriptionForm
from .forms import ProjetForm
from .models import Projet_User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def accueil(request):
    return render(request, "accueil.html")

@login_required
def projets(request):
    form = ProjetForm()
    projets_list = Projet_User.objects.filter(utilisateur=request.user)
    return render(request,'projets.html',{"form":form,"projets_list":projets_list})

@login_required
def create_projet(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet_name = form.cleaned_data['name']
            if Projet_User.objects.filter(name=projet_name, utilisateur=request.user).exists():  
                messages.error(request, f"Un projet avec le nom: {projet_name} existe déjà")  
                return redirect('projets')
            else:   
                try:   
                    projet = form.save(commit=False) 
                    projet.utilisateur = request.user 
                    projet.date_de_creation = datetime.now().date()
                    projet.date_de_modification = datetime.now().date()
                    projet.save()  
                    messages.success(request, f"Projet créé avec succès!")
                    return redirect('projets')
                except Exception as e:
                    messages.error(request, f"Erreur pendant la création du projet, {e}")
                    return redirect('projets')
        else:
            messages.error(request,"Erreur lors du chargement du formulaire")  
            return redirect('projets')  
    return redirect('projets')