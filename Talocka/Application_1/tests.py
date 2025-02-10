from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Projet_User

class ProjetTests(TestCase):

    def setUp(self):
        """Créer un utilisateur et un projet"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_projet_view(self):
        """Tester la création d'un projet"""
        self.client.login(username='testuser', password='testpassword')  
        response = self.client.post(reverse('create_projet'), {
            'name': 'Projet Test',
            'description': 'Ceci est un projet de test.'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(Projet_User.objects.filter(name='Projet Test').exists())

    def test_projets_view(self):
        """Tester l'affichage du formulaire de projet"""
        response = self.client.get(reverse('projets'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")  
