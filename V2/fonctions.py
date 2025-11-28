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

def hasher_mdp(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generer_mot_de_passe_aleatoire(longueur=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(longueur))

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

def charger_csv(fichier):
    data = []
    try:
        f = open(fichier, 'r') ### Cela permet d'ouvrir le fichier en mode lecture 
        reader = csv.DictReader(f)
        for ligne in reader:
            data.append(ligne)
        f.close()
    except:
        pass
    return data

def sauvegarder_csv(fichier, data, champs):
    f = open(fichier, 'w', newline='') ### Cette fonction permet d'ouvrir le fichier en mode ecriture
    writer = csv.DictWriter(f, fieldnames=champs)
    writer.writeheader()
    i = 0
    while i < len(data):
        writer.writerow(data[i])
        i = i + 1
    f.close()

def ajouter_ligne_csv(fichier, ligne, champs):
    f = open(fichier, 'a', newline='')
    writer = csv.DictWriter(f, fieldnames=champs)
    writer.writerow(ligne)
    f.close()

def verifier_droit_zone(user, site):
    if user['role'] == 'SUPER_ADMIN':
        return True
    if user['site'] == site:
        return True
    return False ### cette fonction permet d'autoriser les droits aux user et d'acceder uniquement a sont site 

def lister_personnel(current_user, type_cible="users"):
    if type_cible == "users":
        fichier = FILE_USERS
        label = "UTILISATEURS"
    else:
        fichier = FILE_ADMINS
        label = "ADMINISTRATEURS"
    
    data = charger_csv(fichier)
    
    if current_user['role'] != 'SUPER_ADMIN':
        zone = current_user['site']
    else:
        zone = 'Global'
    
    print("\n LISTE DES " + label + " (" + zone + ") ---")
    print("ID  Login  /  Nom   /  Prenom  / Site")
    
    count = 0
    for p in data:
        if verifier_droit_zone(current_user, p['site']) == True:
            print(p['id'] + "     " + p['login'] + "     " + p['nom'] + "     " + p['prenom'] + "     " + p['site'])
            count = count + 1
    
    if count == 0:
        print("Aucun resultat.")

def ajouter_personne(current_user, type_cible="users", generer_login=None, generer_mot_de_passe_aleatoire=None, hasher_mdp=None):
    if current_user['role'] == 'USER':
        return ### Cette fonction permet que USER ne peut rien creer ni ajouter une personne 
    
    print("\n AJOUTER UN NOUVEL UTILISATEUR")
    nom = input("Nom : ")
    prenom = input("Prenom : ") ### Cette fonction permet d'ajouter une personne en remplissant les champs nom et prenom
    
    if current_user['role'] == 'SUPER_ADMIN':
        site = input("Site (Paris/Marseille/Rennes/Grenoble) : ") ### Cette ligne permet que uniquement et seulement le Super Admin peut choisir le site pour le USER
    else:
        site = current_user['site']
        print("Site : " + site)
    
    login = generer_login(nom, prenom)
    pwd = generer_mot_de_passe_aleatoire()
    pwd_hash = hasher_mdp(pwd)
    
    if type_cible == "users":
        fichier = FILE_USERS
        champs = CHAMPS_USERS
    else:
        fichier = FILE_ADMINS
        champs = CHAMPS_ADMINS
    
    data = charger_csv(fichier)
    new_id = len(data) + 1
    
    role = 'USER'
    if type_cible == 'admins':
        if site == 'Paris' and current_user['role'] == 'SUPER_ADMIN':
            role = 'SUPER_ADMIN'
        else:
            role = 'ADMIN'
    
    nouvelle = {'id': new_id, 'login': login, 'password_hash': pwd_hash, 'nom': nom, 'prenom': prenom, 'role': role, 'site': site}
    
    ajouter_ligne_csv(fichier, nouvelle, champs) ### Cette fonction permet d'ajouter le nouvelle utilisateur dans le fichier .csv
    print("OK ! Login: " + login + " / Mdp: " + pwd)

# Modifier personne
def modifier_personne(current_user, type_cible="users"):
    if current_user['role'] == 'USER':
        return
    
    lister_personnel(current_user, type_cible)
    id_modif = input("\nID : ")
    
    if type_cible == "users":
        fichier = FILE_USERS
        champs = CHAMPS_USERS
    else:
        fichier = FILE_ADMINS
        champs = CHAMPS_ADMINS
    
    data = charger_csv(fichier)
    
    trouve = False
    for p in data:
        if p['id'] == id_modif:
            if not verifier_droit_zone(current_user, p['site']): ### Cette action permet de verifier si la personne a les droits pour modifier
                print("Vous n'avez pas les droits necessaire .")
                return
            
            if p['role'] == 'SUPER_ADMIN' and current_user['role'] != 'SUPER_ADMIN': ### Il est impossible de modifier Super Admin sans etre un Super Admin> 
                print(" Il pas possible de toucher au Super Admin.")
                return
            
            nouveau = input("Nouveau nom : ")
            if nouveau != "":
                p['nom'] = nouveau
            trouve = True
            break
    
    if trouve == True:
        sauvegarder_csv(fichier, data, champs) ### Si le nom a ete modifier il reecrit le fichier complet avec la modification
        print("Modifie.")
    else:
        print("Pas trouve.")

def supprimer_personne(current_user, type_cible="users"):
    if current_user['role'] == 'USER':
        return ### Si un USER essaye de supprimer un users il ne pourra pas car il n'est pas super admin ou admin
    
    lister_personnel(current_user, type_cible)
    id_sup = input("\nID : ")
    
    if type_cible == "users":
        fichier = FILE_USERS
        champs = CHAMPS_USERS
    else:
        fichier = FILE_ADMINS
        champs = CHAMPS_ADMINS
    
    data = charger_csv(fichier)
    nouvelle_liste = []
    supprime = False
    
    for p in data:
        if p['id'] == id_sup:
            if verifier_droit_zone(current_user, p['site']) == True:
                if p['login'] == current_user['login']:
                    print("No Suicide Please !!! .")
                    nouvelle_liste.append(p)
                elif p['role'] == 'SUPER_ADMIN' and current_user['role'] != 'SUPER_ADMIN':
                    print("Ta pas le droit toucher !!!  .")
                    nouvelle_liste.append(p)
                else:
                    print("Supprime : " + p['login'])
                    supprime = True 
            else:
                print("Vous n'avez pas les droits necessaire !!! .")
                nouvelle_liste.append(p)
        else:
            nouvelle_liste.append(p)
    
    if supprime == True:
        sauvegarder_csv(fichier, nouvelle_liste, champs) ### On peut reecrire le fichier sans la personne supprimer