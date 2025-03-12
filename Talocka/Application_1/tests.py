from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from Application_1.models import Projet_User, DatasetMetadata
from bson import ObjectId





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

        self.projet = Projet_User.objects.create(
            name="Projet Test",
            description="Projet pour tester MongoDB",
            utilisateur=self.user
        )

    @patch('Application_1.utils.get_mongo_gridfs')
    def test_upload_dataset(self, mock_get_mongo_gridfs):
        """Tester l'upload d'un dataset dans MongoDB"""
        mock_db = MagicMock()
        mock_grid_fs = MagicMock()
        mock_file_id = ObjectId()  # Génère un ObjectId correct

        mock_grid_fs.put.return_value = mock_file_id
        mock_get_mongo_gridfs.return_value = (mock_db, mock_grid_fs)

        file_mock = MagicMock()
        file_mock.name = "test_file.csv"
        file_mock.read.return_value = b"data"

        response = self.client.post(reverse('upload_dataset', args=[self.projet.id]), {
            'dataset_name': 'Dataset Test',
            'description': 'Un dataset de test',
            'file': file_mock
        })

        self.assertEqual(response.status_code, 302)
        dataset = DatasetMetadata.objects.get(projet=self.projet, dataset_name="Dataset Test")
        self.assertEqual(str(dataset.file_id), str(mock_file_id))  # Correction


    @patch('Application_1.utils.get_mongo_gridfs')
    def test_delete_dataset(self, mock_get_mongo_gridfs):
        """Tester la suppression d'un dataset dans MongoDB"""
        mock_db = MagicMock()
        mock_grid_fs = MagicMock()
        mock_get_mongo_gridfs.return_value = (mock_db, mock_grid_fs)

        dataset = DatasetMetadata.objects.create(
            projet=self.projet,
            dataset_name="Dataset à Supprimer",
            description="Un dataset temporaire",
            file_id=str(ObjectId())
        )

        response = self.client.post(reverse('delete_dataset', args=[dataset.id]))

        # Vérification que le dataset est supprimé
        self.assertEqual(response.status_code, 302)
        self.assertFalse(DatasetMetadata.objects.filter(id=dataset.id).exists())

        # Vérifier que GridFS a bien supprimé le fichier
        mock_grid_fs.delete.assert_called_once_with(ObjectId(dataset.file_id))
