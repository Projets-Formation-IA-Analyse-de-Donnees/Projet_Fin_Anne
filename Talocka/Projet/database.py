import mongoengine
# MONGO_URI, MONGO_DB_NAME, MONGO_USERNAME, MONGO_PASSWORD, MONGO_AUTH_SOURCE

def connect_to_mongodb():
    """
    Se connecte à MongoDB en utilisant les paramètres définis dans settings.py.
    """
    mongoengine.connect(
    db='mydb',  
    username='mongo',
    password='mongo',
    host='mongodb://mongodb:27017/mydb', 
    authentication_source='admin',  
)

from mongoengine import Document, StringField


# Appeler la fonction de connexion avant de travailler avec les modèles
connect_to_mongodb()

# Définir un modèle MongoDB
class Projet(Document):
    name = StringField()
    

# Fonction pour ajouter un utilisateur
def add_user(name, email):
    user = Projet(name=name, email=email)