import os

# Fichiers CSV
USERS_FILE = "data/users.csv"
ADMINS_FILE = "data/admins.csv"

# Noms des colonnes
USERS_FIELDS = ["id", "prenom", "nom", "login", "role"]

ADMINS_FIELDS = [
    "id",
    "prenom",
    "nom",
    "login",
    "region",
    "is_superadmin",   # "True" ou "False"
    "pwd_hash",
    "pwd_expires_at"
]


def init_storage():
    """
    Crée le dossier data/ et les fichiers CSV
    avec la ligne d'en-tête s'ils n'existent pas.
    """
    # Créer le dossier data s'il n'existe pas
    if not os.path.exists("data"):
        os.mkdir("data")

    # Fichier des utilisateurs
    if not os.path.exists(USERS_FILE):
        f = open(USERS_FILE, "w")
        f.write(";".join(USERS_FIELDS) + "\n")
        f.close()

    # Fichier des administrateurs
    if not os.path.exists(ADMINS_FILE):
        f = open(ADMINS_FILE, "w")
        f.write(";".join(ADMINS_FIELDS) + "\n")
        f.close()


def load_users():
    """
    Retourne la liste des utilisateurs (liste de dictionnaires).
    """
    users = []

    # Si le fichier n'existe pas
    if not os.path.exists(USERS_FILE):
        return users

    f = open(USERS_FILE, "r")
    lignes = f.readlines()
    f.close()

    # S'il n'y a que l'entête ou rien
    if len(lignes) <= 1:
        return users

    # Première ligne : entête
    entete = lignes[0].strip().split(";")

    # Lignes suivantes : données
    for ligne in lignes[1:]:
        ligne = ligne.strip()
        if ligne == "":
            continue

        valeurs = ligne.split(";")
        user = {}

        # Associer chaque colonne à sa valeur
        for i in range(len(entete)):
            nom_colonne = entete[i]
            if i < len(valeurs):
                user[nom_colonne] = valeurs[i]
            else:
                user[nom_colonne] = ""

        users.append(user)

    return users


def save_users(users):
    """
    Sauvegarde la liste d'utilisateurs dans users.csv
    (users est une liste de dictionnaires).
    """
    f = open(USERS_FILE, "w")
    # Entête
    f.write(";".join(USERS_FIELDS) + "\n")

    # Données
    for user in users:
        valeurs = []
        for champ in USERS_FIELDS:
            if champ in user:
                valeur = str(user[champ])
            else:
                valeur = ""
            # éviter les ';' dans les valeurs
            valeur = valeur.replace(";", ",")
            valeurs.append(valeur)

        ligne = ";".join(valeurs)
        f.write(ligne + "\n")

    f.close()


def load_admins():
    """
    Retourne la liste des administrateurs (liste de dictionnaires).
    """
    admins = []

    if not os.path.exists(ADMINS_FILE):
        return admins

    f = open(ADMINS_FILE, "r")
    lignes = f.readlines()
    f.close()

    if len(lignes) <= 1:
        return admins

    entete = lignes[0].strip().split(";")

    for ligne in lignes[1:]:
        ligne = ligne.strip()
        if ligne == "":
            continue

        valeurs = ligne.split(";")
        admin = {}

        for i in range(len(entete)):
            nom_colonne = entete[i]
            if i < len(valeurs):
                admin[nom_colonne] = valeurs[i]
            else:
                admin[nom_colonne] = ""

        admins.append(admin)

    return admins


def save_admins(admins):
    """
    Sauvegarde la liste d'admins dans admins.csv
    (admins est une liste de dictionnaires).
    """
    f = open(ADMINS_FILE, "w")
    f.write(";".join(ADMINS_FIELDS) + "\n")

    for admin in admins:
        valeurs = []
        for champ in ADMINS_FIELDS:
            if champ in admin:
                valeur = str(admin[champ])
            else:
                valeur = ""
            valeur = valeur.replace(";", ",")
            valeurs.append(valeur)

        ligne = ";".join(valeurs)
        f.write(ligne + "\n")

    f.close()
