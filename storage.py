import os

USERS_FILE = "data/users.csv"
ADMINS_FILE = "data/admins.csv"

# Colonnes communes aux deux CSV (alignées avec CHAMPS_USERS / CHAMPS_ADMINS du Dev2)
USERS_FIELDS = ['id', 'login', 'password_hash', 'nom', 'prenom', 'role', 'site']
ADMINS_FIELDS = ['id', 'login', 'password_hash', 'nom', 'prenom', 'role', 'site']


def init_storage():
    """Crée le dossier data/ et les fichiers CSV avec l'entête s'ils n'existent pas."""
    os.makedirs("data", exist_ok=True)
    for path, fields in ((USERS_FILE, USERS_FIELDS),
                         (ADMINS_FILE, ADMINS_FIELDS)):
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(";".join(fields) + "\n")


def _load(path, fields):
    """Charge un fichier CSV simple et renvoie une liste de dictionnaires."""
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    if len(lines) <= 1:
        return []

    rows = []
    for line in lines[1:]:  # on saute l'entête
        if line == "":
            continue
        values = line.split(";")
        d = {}
        for i, field in enumerate(fields):
            d[field] = values[i] if i < len(values) else ""
        rows.append(d)
    return rows


def _save(path, fields, rows):
    """Réécrit complètement un CSV à partir d'une liste de dictionnaires."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(";".join(fields) + "\n")  # entête
        for d in rows:
            values = []
            for field in fields:
                v = str(d.get(field, ""))
                v = v.replace(";", ",")
                values.append(v)
            f.write(";".join(values) + "\n")


def load_users():
    """Liste d'utilisateurs (list[dict]) depuis users.csv."""
    return _load(USERS_FILE, USERS_FIELDS)


def save_users(users):
    """Sauvegarde la liste d'utilisateurs dans users.csv."""
    _save(USERS_FILE, USERS_FIELDS, users)


def load_admins():
    """Liste d'admins (list[dict]) depuis admins.csv."""
    return _load(ADMINS_FILE, ADMINS_FIELDS)


def save_admins(admins):
    """Sauvegarde la liste d'admins dans admins.csv."""
    _save(ADMINS_FILE, ADMINS_FIELDS, admins)


# ==== WRAPPERS POUR LE CODE DU DEV2 (users_admins.py) ====

def charger_csv(fichier):
    """Wrapper utilisé par Dev2 : renvoie list[dict] en fonction du fichier."""
    if fichier == USERS_FILE:
        return load_users()
    if fichier == ADMINS_FILE:
        return load_admins()
    return []


def ajouter_ligne_csv(fichier, nouvelle_personne, champs):
    """Wrapper utilisé par Dev2 pour ajouter une ligne et sauvegarder."""
    if fichier == USERS_FILE:
        data = load_users()
        data.append(nouvelle_personne)
        save_users(data)
    elif fichier == ADMINS_FILE:
        data = load_admins()
        data.append(nouvelle_personne)
        save_admins(data)


def sauvegarder_csv(fichier, data, champs):
    """Wrapper utilisé par Dev2 pour réécrire un CSV complet."""
    if fichier == USERS_FILE:
        save_users(data)
    elif fichier == ADMINS_FILE:
        save_admins(data)


# ===== NOTE RAPIDE POUR DEV1 / DEV2 =====
# - Fichiers utilisés :
#     data/users.csv  et data/admins.csv
# - Colonnes :
#     id;login;password_hash;nom;prenom;role;site
# - Vous travaillez sur des listes de dict en mémoire,
#   et c'est storage.py qui gère la lecture / écriture CSV.
# ========================================
