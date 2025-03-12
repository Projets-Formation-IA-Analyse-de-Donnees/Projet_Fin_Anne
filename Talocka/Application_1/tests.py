from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock,Mock
from Application_1.models import Projet_User, DatasetMetadata
from bson import ObjectId
from .forms import DatasetUploadForm
from django.core.files.uploadedfile import SimpleUploadedFile




class ProjetTests(TestCase):

    def setUp(self):
        """Créer un utilisateur et un projet de test"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Création d'un projet existant
        self.projet = Projet_User.objects.create(
            name="Projet Existant",
            description="Description du projet existant.",
            utilisateur=self.user
        )

    def test_projets_view(self):
        """Tester l'affichage de la page des projets"""
        response = self.client.get(reverse('projets'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")  # Vérifie que le formulaire est présent
        self.assertContains(response, "Projet Existant")  # Vérifie que le projet existant est affiché

    def test_create_projet_view(self):
        """Tester la création d'un projet"""
        response = self.client.post(reverse('create_projet'), {
            'name': 'Projet Test',
            'description': 'Ceci est un projet de test.'
        })

        # Vérifier la redirection après création
        self.assertEqual(response.status_code, 302)  
        
        # Vérifier que le projet a bien été créé
        self.assertTrue(Projet_User.objects.filter(name='Projet Test', utilisateur=self.user).exists())

    def test_create_duplicate_projet(self):
        """Tester la création d'un projet en double (même nom)"""
        # Supprimer un projet existant s'il existe
        Projet_User.objects.filter(name="Projet Existant", utilisateur=self.user).delete()

        response = self.client.post(reverse('create_projet'), {
            'name': 'Projet Existant',  # Nom déjà utilisé
            'description': 'Tentative de création en double'
        })

        # Vérifier la redirection après erreur
        self.assertEqual(response.status_code, 302)  
        
        # Vérifier que le projet en double n'a pas été créé
        self.assertEqual(Projet_User.objects.filter(name="Projet Existant", utilisateur=self.user).count(), 1)



class MongoDBTests(TestCase):

    def setUp(self):
        """Créer un utilisateur et un projet de test"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Créer un projet si nécessaire
        if not Projet_User.objects.filter(name="Projet Test", utilisateur=self.user).exists():
            self.projet = Projet_User.objects.create(
                name="Projet Test",
                description="Projet pour tester MongoDB",
                utilisateur=self.user
            )


   

    def test_upload_dataset(self, mock_get_mongo_gridfs):
        """ Tester l'upload d'un dataset dans MongoDB """

        mock_db = Mock()
        mock_grid_fs = Mock()

        # Simuler un ObjectId correct
        mock_file_id = ObjectId()  
        mock_grid_fs.put.return_value = mock_file_id  # GridFS retourne cet ID

        mock_get_mongo_gridfs.return_value = (mock_db, mock_grid_fs)

        # Créer un fichier en mémoire pour l'upload
        file = SimpleUploadedFile("test.txt", b"Contenu test", content_type="text/plain")

        response = self.client.post(reverse("upload_dataset", args=[self.projet.id]), {
            "dataset_name": "Test Dataset",
            "description": "Dataset de test",
            "file": file  # Utiliser le fichier ici
        })

        # Vérification de la redirection
        self.assertEqual(response.status_code, 302)

        dataset = DatasetMetadata.objects.get(dataset_name="Test Dataset")
        
        # Comparer les IDs sous forme de chaîne
        self.assertEqual(str(dataset.file_id), str(mock_file_id))




    @patch("Application_1.views.get_mongo_gridfs")  # Mock MongoDB
    def test_delete_dataset(self, mock_get_mongo_gridfs):
        """ Tester la suppression d'un dataset dans MongoDB """

        # Mock de GridFS
        mock_db = Mock()
        mock_grid_fs = Mock()
        mock_get_mongo_gridfs.return_value = (mock_db, mock_grid_fs)

        # Création d’un projet et d’un dataset
        projet = Projet_User.objects.create(
            name="Projet Test",
            utilisateur=self.user
        )

        dataset = DatasetMetadata.objects.create(
            projet=projet,
            dataset_name="Test Dataset",
            file_id=str(ObjectId())  # Un ID valide
        )

        # Appel de l'endpoint de suppression
        response = self.client.post(reverse("delete_dataset", args=[dataset.id]))

        # Vérification de la redirection
        self.assertEqual(response.status_code, 302)

        # **Correction ici** : Vérifier que `delete` a été appelé
        mock_grid_fs.delete.assert_called_once_with(ObjectId(dataset.file_id))

        # Vérifier que le dataset a bien été supprimé
        self.assertFalse(DatasetMetadata.objects.filter(id=dataset.id).exists())
