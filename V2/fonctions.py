import csv              #On importe le module csv ( sert a lire et écire des files au format csv) (texte avec des valeurs séparées par des virgules)
import os               #permet d'interagir avec l'os (vérifier si un fichier existe, effacer l'écran, etc.)
import hashlib          #sert à "hacher" des mots de passe 
import random           #sert à générer des valeurs aléatoires
import string           #contient des constantes utiles pour les chaînes de caractères (alphabet, chiffres, etc.)
import platform         # permet de connaître des infos sur le système (Windows, Linux, etc.)


# --- CONSTANTES ---
FILE_ADMINS = "data/admins.csv"     #Fichier des administrateurs
FILE_USERS = "data/users.csv"       #Fichier des utilisateurs
CHAMPS_ADMINS = ['id', 'login', 'password_hash', 'nom', 'prenom', 'role', 'site'] #noms de collones pour les admins
CHAMPS_USERS = ['id', 'login', 'password_hash', 'nom', 'prenom', 'role', 'site'] #noms de collones pour les utilisateurs

# --- PARTIE 1 : UTILITAIRES & STOCKAGE ---

def effacer_ecran():
    """Nettoie la console."""
    # Choix de la commande selon le système
    if platform.system() == 'Windows':
        os.system('cls') # Effacer l'écran sous Windows
    else:
        os.system('clear') # Effacer l'écran sous Linux/Mac

def pause():
    input("\nAppuyez sur Entrée pour continuer...")

def charger_csv(chemin_fichier):
    """Lit un CSV et renvoie une liste de dicts."""
    data = [] # Liste qui contiendra les lignes
    
    if not os.path.exists(chemin_fichier):
          # Si le fichier n'existe pas, on renvoie une liste vide
        return data
    try:
        with open(chemin_fichier, mode='r', encoding='utf-8', newline='') as f:
             # Ouverture du fichier en lecture texte
             
            reader = csv.DictReader(f) # Chaque ligne = dict (colonne: valeur)
            for row in reader:
                data.append(row)       # Ajout de la ligne dans la liste
                
    except Exception as e:
        # Affiche l'erreur en cas de problème
        print(f"Erreur lecture {chemin_fichier}: {e}")
        
    return data # Renvoie toutes les lignes lues

def sauvegarder_csv(chemin_fichier, data, fieldnames):
    """Écrase le CSV avec les nouvelles données."""
    try:
        with open(chemin_fichier, mode='w', encoding='utf-8', newline='') as f:
             # Ouverture en écriture (écrase le fichier)
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader() # Écrit la ligne d'en-tête (colonnes)
            writer.writerows(data) # Écrit toutes les lignes (liste de dicts)
            
    except Exception as e:
        # Affiche l'erreur en cas de problème
        print(f"Erreur écriture {chemin_fichier}: {e}")

def ajouter_ligne_csv(chemin_fichier, ligne_dict, fieldnames):
    """Ajoute une ligne à la fin du CSV."""
    file_exists = os.path.exists(chemin_fichier) # Le fichier existe déjà ?
    try:
        with open(chemin_fichier, mode='a', encoding='utf-8', newline='') as f:
            # Ouverture en ajout (append)
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                # Si le fichier est nouveau, on ajoute l'en-tête
                writer.writeheader()
                
            writer.writerow(ligne_dict) # Ajoute une seule ligne (un dict)
    except Exception as e:
         # Affiche l'erreur en cas de problème
        print(f"Erreur ajout {chemin_fichier}: {e}")

# --- PARTIE 2 : SÉCURITÉ & AUTHENTIFICATION ---

# def hasher_mdp(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def generer_mot_de_passe_aleatoire(longueur=12):
#     chars = string.ascii_letters + string.digits + string.punctuation
#     return ''.join(random.choice(chars) for _ in range(longueur))

liste_de_caracteres=string.ascii_letters+string.digits+string.punctuation
### initialisation du pwd à générer aléatoirement
def generer_mot_de_passe_aleatoire():
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
    if not nom or not prenom: return "inconnu"  # Si l'un des deux champs sont vides le login sera inconnu
    return f"{prenom[0].lower()}{nom.lower().replace(' ', '')}" 
### Cette fonction permet de generer le login en prenant la premiere lettre du prenom en minuscule et le nom en minuscule aussi en supprimant les espaces
### Exemple : Nom: Dupond Prenom: Jean => Login: jdupond

def login_systeme():
    """Gère la connexion et renvoie la session utilisateur."""
    print("=== AUTHENTIFICATION AMERICAN HOSPITAL ===")
    user_login = input("Login : ").strip() ### saisi du login de l'utilisateur | le .strip() permet de supprimer les espaces avant et apres le login
    user_pwd = input("Mot de passe : ").strip() ### saisi du mot de passe de l'utilisateur
    pwd_hash = hasher_mdp(user_pwd) ### Cette ligne permet de hasher le mot de passe saisi par l'utilisateur

    # 1. verfication administrateur
    admins = charger_csv(FILE_ADMINS) ### Cette fonction permet de charger le fichier admin.csv
    for admin in admins:
        if admin['login'] == user_login and admin['password_hash'] == pwd_hash:
            return admin ### Si les identifiants match bien avec le fihcier il retourne l'admin connecté sinon il passe a l'etape suivante
    
    # 2. Check Users
    users = charger_csv(FILE_USERS) ### Cette fonction permet de charger le fichier users.csv
    for user in users:
        if user['login'] == user_login and user['password_hash'] == pwd_hash:
            if user.get('role') is None: user['role'] = 'USER' ### Cette ligne vérifie si le role de l'utilisateur est vide si oui alors il le remplit par defaut avec USER
            return user ### Si les identifiants match bien avec le fihcier il retourne l'user connecté sinon il passe a l'etape suivante

    print("Identifiants incorrects.")
    return None ### Si les identifiants ne match ni avec le fichiers users ou admins alors il retourne None

def verifier_droit_zone(current_user, cible_site):
    ## 1. On recupere les infos de l'utilisateur actuel et on les met ds 2 variables
    mon_role = current_user['role'] 
    mon_site = current_user['site'] 

    ## 2. On verifie les droits
    if mon_role == 'SUPER_ADMIN':
        return True  ### C le patron on accepte tout de suite
    
    elif mon_site == cible_site: 
        return True  ### C le bon site on accepte
        
    else:
        return False # Sinon, c'est refusé

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

def ajouter_personne(current_user,type_cible="users"): ### Cette fonction permet d'ajouter un utilisateur sauf si la personne est a le role USER elle ne peut pas creer un autre utilisateur.
    if current_user['role'] == 'USER':
        return 
    
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
                print("Tu as pas les droits necessaire !!! .")
                return
            
            if p['role'] == 'SUPER_ADMIN' and current_user['role'] != 'SUPER_ADMIN': ### Il est impossible de modifier Super Admin sans etre un Super Admin> 
                print(" Tu peus pas toucher au Super Admin !!! .")
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
                    print("Tu peu pas te supprimer toi meme !!!  .")
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