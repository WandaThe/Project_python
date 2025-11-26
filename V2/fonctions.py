import csv
import os
import hashlib
import random
import string
import platform
import time

# --- CONSTANTES ---
FILE_ADMINS = "data/admins.csv"
FILE_USERS = "data/users.csv"
CHAMPS_ADMINS = ['id', 'login', 'password_hash', 'nom', 'prenom', 'role', 'site']
CHAMPS_USERS = ['id', 'login', 'password_hash', 'nom', 'prenom', 'role', 'site']

# --- PARTIE 1 : UTILITAIRES & STOCKAGE ---

def effacer_ecran():
    """Nettoie la console."""
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def pause():
    input("\nAppuyez sur Entrée pour continuer...")

def charger_csv(chemin_fichier):
    """Lit un CSV et renvoie une liste de dicts."""
    data = []
    if not os.path.exists(chemin_fichier):
        return data
    try:
        with open(chemin_fichier, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Erreur lecture {chemin_fichier}: {e}")
    return data

def sauvegarder_csv(chemin_fichier, data, fieldnames):
    """Écrase le CSV avec les nouvelles données."""
    try:
        with open(chemin_fichier, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f"Erreur écriture {chemin_fichier}: {e}")

def ajouter_ligne_csv(chemin_fichier, ligne_dict, fieldnames):
    """Ajoute une ligne à la fin du CSV."""
    file_exists = os.path.exists(chemin_fichier)
    try:
        with open(chemin_fichier, mode='a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(ligne_dict)
    except Exception as e:
        print(f"Erreur ajout {chemin_fichier}: {e}")

# --- PARTIE 2 : SÉCURITÉ & AUTH ---

# def hasher_mdp(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def generer_mot_de_passe_aleatoire(longueur=12):
#     chars = string.ascii_letters + string.digits + string.punctuation
#     return ''.join(random.choice(chars) for _ in range(longueur))

liste_de_caracteres=string.ascii_letters+string.digits+string.punctuation
### initialisation du pwd à générer aléatoirement
def generer_mot_de_passe_aleatoire(passwd):
    passwd=""
    for i in range(12): ### de taille 12 en dur ou bien saisir la size
        ###print("Saisir la Taille du PWD :")
        ''' size=int(input())'''
        #passwd=passwd+liste_de_caracteres[random.randint(0,len(liste_de_caracteres)-1)]
        
        #### en version raccourci
        passwd+=liste_de_caracteres[random.randint(0,len(liste_de_caracteres)-1)]
    print("Le mot de passe généré (à transmettre):", passwd)
    return passwd   
####Hashage en sha256 du mot de passe généré aléatoirement

def hasher_mdp(password):
    mot_de_passe_hashé = hashlib.sha256(password.encode()).hexdigest()
    print("\n mot de pass hashé: " , mot_de_passe_hashé)
    return mot_de_passe_hashé


def generer_login(nom, prenom):
    if not nom or not prenom: return "inconnu"
    return f"{prenom[0].lower()}{nom.lower().replace(' ', '')}"

def login_systeme():
    """Gère la connexion et renvoie la session utilisateur."""
    print("=== AUTHENTIFICATION AMERICAN HOSPITAL ===")
    user_login = input("Login : ").strip()
    user_pwd = input("Mot de passe : ").strip()
    pwd_hash = hasher_mdp(user_pwd)

    # 1. Check Admins
    admins = charger_csv(FILE_ADMINS)
    for admin in admins:
        if admin['login'] == user_login and admin['password_hash'] == pwd_hash:
            return admin
    
    # 2. Check Users
    users = charger_csv(FILE_USERS)
    for user in users:
        if user['login'] == user_login and user['password_hash'] == pwd_hash:
            if user.get('role') is None: user['role'] = 'USER'
            return user

    print("❌ Identifiants incorrects.")
    return None

def verifier_droit_zone(current_user, cible_site):
    """Vrai si l'admin a le droit sur ce site."""
    if current_user['role'] == 'SUPER_ADMIN': return True
    if current_user['site'] == cible_site: return True
    return False

# --- PARTIE 3 : CRUD METIER ---

def lister_personnel(current_user, type_cible="users"):
    fichier = FILE_USERS if type_cible == "users" else FILE_ADMINS
    data = charger_csv(fichier)
    
    label = "UTILISATEURS" if type_cible == "users" else "ADMINISTRATEURS"
    print(f"\n--- LISTE DES {label} ({current_user['site'] if current_user['role'] != 'SUPER_ADMIN' else 'Global'}) ---")
    print(f"{'ID':<5} {'Login':<15} {'Nom':<15} {'Prénom':<15} {'Site':<10}")
    print("-" * 60)

    count = 0
    for p in data:
        if verifier_droit_zone(current_user, p['site']):
            print(f"{p['id']:<5} {p['login']:<15} {p['nom']:<15} {p['prenom']:<15} {p['site']:<10}")
            count += 1
    if count == 0: print(f"Aucun {type_cible[:-1]} trouvé dans votre zone.")

def ajouter_personne(current_user, type_cible="users"):
    if current_user['role'] == 'USER': return

    print(f"\n--- AJOUTER UN {type_cible[:-1].upper()} ---")
    nom = input("Nom : ").strip()
    prenom = input("Prénom : ").strip()
    
    # Site forcé pour admin régional
    if current_user['role'] == 'SUPER_ADMIN':
        site = input("Site (Paris, Marseille, Rennes, Grenoble) : ").strip()
    else:
        site = current_user['site']
        print(f"📍 Site forcé : {site}")

    login = generer_login(nom, prenom)
    pwd_clair = generer_mot_de_passe_aleatoire()
    pwd_hash = hasher_mdp(pwd_clair)
    
    fichier = FILE_USERS if type_cible == "users" else FILE_ADMINS
    champs = CHAMPS_USERS if type_cible == "users" else CHAMPS_ADMINS
    data = charger_csv(fichier)
    new_id = len(data) + 1 

    role_assigne = 'USER'
    if type_cible == 'admins':
        role_assigne = 'SUPER_ADMIN' if site == 'Paris' and current_user['role'] == 'SUPER_ADMIN' else 'ADMIN'

    nouvelle_personne = {
        'id': new_id, 'login': login, 'password_hash': pwd_hash,
        'nom': nom, 'prenom': prenom, 'role': role_assigne, 'site': site
    }

    ajouter_ligne_csv(fichier, nouvelle_personne, champs)
    print(f"✅ Créé ! Login: {login} | Mdp: {pwd_clair}")

def modifier_personne(current_user, type_cible="users"):
    if current_user['role'] == 'USER': return
    lister_personnel(current_user, type_cible)
    id_modif = input("\nID à modifier : ").strip()
    
    fichier = FILE_USERS if type_cible == "users" else FILE_ADMINS
    champs = CHAMPS_USERS if type_cible == "users" else CHAMPS_ADMINS
    data = charger_csv(fichier)
    
    trouve = False
    for p in data:
        if str(p['id']) == id_modif:
            if not verifier_droit_zone(current_user, p['site']):
                print("⛔ Hors zone."); return
            
            # Protection Super Admin
            if p['role'] == 'SUPER_ADMIN' and current_user['role'] != 'SUPER_ADMIN':
                print("⛔ Impossible de modifier le Super Admin."); return

            nouveau_nom = input(f"Nouveau nom ({p['nom']}) : ").strip()
            if nouveau_nom: p['nom'] = nouveau_nom
            trouve = True; break
    
    if trouve:
        sauvegarder_csv(fichier, data, champs)
        print("✅ Modifié.")
    else:
        print("❌ Non trouvé.")

def supprimer_personne(current_user, type_cible="users"):
    if current_user['role'] == 'USER': return
    lister_personnel(current_user, type_cible)
    id_suppr = input("\nID à supprimer : ").strip()
    
    fichier = FILE_USERS if type_cible == "users" else FILE_ADMINS
    champs = CHAMPS_USERS if type_cible == "users" else CHAMPS_ADMINS
    data = charger_csv(fichier)
    nouvelle_liste = []
    
    supprime = False
    for p in data:
        if str(p['id']) == id_suppr:
            if verifier_droit_zone(current_user, p['site']):
                if p['login'] == current_user['login']:
                    print("⛔ Suicide interdit."); nouvelle_liste.append(p)
                elif p['role'] == 'SUPER_ADMIN' and current_user['role'] != 'SUPER_ADMIN':
                    print("⛔ Super Admin intouchable."); nouvelle_liste.append(p)
                else:
                    print(f"🗑 Supprimé : {p['login']}"); supprime = True
            else:
                print("⛔ Hors zone."); nouvelle_liste.append(p)
        else:
            nouvelle_liste.append(p)

    if supprime: sauvegarder_csv(fichier, nouvelle_liste, champs)