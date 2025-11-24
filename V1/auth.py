import hashlib
import random
import string
import storage

# Chemins des fichiers
FILE_ADMINS = "data/admins.csv"
FILE_USERS = "data/users.csv"

def hasher_mdp(password):
    """Retourne le hash SHA-256 du mot de passe."""
    return hashlib.sha256(password.encode()).hexdigest()

def generer_mot_de_passe_aleatoire(longueur=12):
    """Génère un mot de passe aléatoire robuste."""
    caracteres = string.ascii_letters + string.digits + string.punctuation 
    return ''.join(random.choice(caracteres) for i in range(longueur))

def login_systeme():
    """
    Demande login/mdp et vérifie les accès.
    Retourne un dictionnaire session ou None.
    """
    print("=== AUTHENTIFICATION AMERICAN HOSPITAL ===")
    user_login = input("Login : ").strip()
    user_pwd = input("Mot de passe : ").strip()
    pwd_hash = hasher_mdp(user_pwd)

    # 1. Vérifier dans les Admins d'abord
    admins = storage.charger_csv(FILE_ADMINS)
    for admin in admins:
        if admin['login'] == user_login and admin['password_hash'] == pwd_hash:
            return admin  # Retourne tout le profil (role, site, etc.)

    # 2. Vérifier dans les Users
    users = storage.charger_csv(FILE_USERS)
    for user in users:
        if user['login'] == user_login and user['password_hash'] == pwd_hash:
            # Un user simple ne peut pas être un admin déguisé
            if user.get('role') is None: 
                user['role'] = 'USER' # Sécurité par défaut
            return user

    print("Identifiants incorrects.")
    return None