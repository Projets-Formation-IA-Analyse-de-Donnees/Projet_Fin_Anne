from django.shortcuts import render
from django.shortcuts import render, redirect
from datetime import datetime
# from .forms import ConnexionForm,InscriptionForm
from .forms import ProjetForm
from .models import Projet_User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404

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

@login_required
def modifier_projet(request, projet_id):
    projet = get_object_or_404(Projet_User, id=projet_id, utilisateur=request.user)

    if request.method == "POST":
        form = ProjetForm(request.POST)  
        return render(request, 'modifier_projet.html', {'form': form, 'projet': projet})

    else:
        return redirect('projets') 

@login_required
def modification(request,projet_id) :
    projet = get_object_or_404(Projet_User, id=projet_id, utilisateur=request.user)
    if request.method == 'POST':
        form = ProjetForm(request.POST, instance=projet) 
        if form.is_valid():
            form.save()
            messages.success(request, "Projet modifié avec succès !")
            return redirect('projets')  

        else:
            messages.error(request, "Erreur lors de la modification du projet. Veuillez corriger les erreurs ci-dessous.")
            return render(request, 'modifier_projet.html', {'form': form, 'projet': projet})

@login_required
def delete_projet(request):
    if request.method == 'POST':
        Supprimer = request.POST.get('Supprimer',None)
        if Supprimer:
            projet = get_object_or_404(Projet_User, id=Supprimer, utilisateur=request.user)
            projet.delete()
            messages.success(request, "Projet supprimé avec succès !")
            return redirect('projets')  
        else:
            messages.success(request, "Projet non trouvé")
            return redirect('projets')  

    return redirect('projets')