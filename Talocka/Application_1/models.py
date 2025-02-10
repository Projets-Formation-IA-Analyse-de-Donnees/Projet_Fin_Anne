from django.db import models

# Create your models here.
class Projet_User(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    date_de_creation = models.DateField(auto_now_add=True)
    date_de_modification = models.DateField(auto_now=True)
    utilisateur = models.ForeignKey('auth.User',on_delete=models.CASCADE)
