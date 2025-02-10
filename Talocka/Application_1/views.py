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

def create_projet(request):
    if request.method=='POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            uder_id = request.user.id
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            now = datetime.now().date()
            projet = Projet_User.objects.create(
            name= name,
            description=description,
            date_de_creation = now,
            date_de_modification = now,
            utilisateur=request.user    
)
            print("go")
        return redirect('projets')
    else:
        form = ProjetForm()
        return redirect('projets')