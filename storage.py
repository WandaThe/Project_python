import os

USERS_FILE = "data/users.csv"
ADMINS_FILE = "data/admins.csv"

USERS_FIELDS = ["id", "prenom", "nom", "login", "role"]
ADMINS_FIELDS = [
    "id", "prenom", "nom", "login",
    "region", "is_superadmin", "pwd_hash", "pwd_expires_at"
]


def init_storage():
    os.makedirs("data", exist_ok=True)
    for path, fields in ((USERS_FILE, USERS_FIELDS),
                         (ADMINS_FILE, ADMINS_FIELDS)):
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(";".join(fields) + "\n")


def _load(path, fields):
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    if len(lines) <= 1:
        return []

    rows = []
    for line in lines[1:]:      # on saute l'entête
        if line == "":
            continue
        values = line.split(";")
        d = {}
        for i, field in enumerate(fields):
            d[field] = values[i] if i < len(values) else ""
        rows.append(d)
    return rows


def _save(path, fields, rows):
    with open(path, "w", encoding="utf-8") as f:
        f.write(";".join(fields) + "\n")      # entête
        for d in rows:
            values = []
            for field in fields:
                v = str(d.get(field, ""))
                v = v.replace(";", ",")
                values.append(v)
            f.write(";".join(values) + "\n")


def load_users():
    return _load(USERS_FILE, USERS_FIELDS)


def save_users(users):
    _save(USERS_FILE, USERS_FIELDS, users)


def load_admins():
    return _load(ADMINS_FILE, ADMINS_FIELDS)


def save_admins(admins):
    _save(ADMINS_FILE, ADMINS_FIELDS, admins)


# - Ce module gère UNIQUEMENT le stockage en CSV, via deux fichiers :
#     data/users.csv  (colonnes : id;prenom;nom;login;role)
#     data/admins.csv (colonnes : id;prenom;nom;login;region;is_superadmin;pwd_hash;pwd_expires_at)
#
# - Fonctions à utiliser :
#     init_storage()        -> crée data/ + les fichiers CSV avec l'entête si besoin
#     load_users()          -> list[dict] d'utilisateurs depuis users.csv
#     save_users(users)     -> réécrit users.csv à partir de la list[dict]
#     load_admins()         -> list[dict] d'admins depuis admins.csv
#     save_admins(admins)   -> réécrit admins.csv à partir de la list[dict]
#
# - Vous travaillez TOUJOURS sur des listes de dictionnaires en mémoire
#   (users_list / admins_list) fournies par main.py.
#
# - C'est main.py qui appelle save_users(...) / save_admins(...)
#   après vos opérations de création / modification / suppression.

