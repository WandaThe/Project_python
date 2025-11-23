import storage
import auth

FILE_ADMINS = "data/admins.csv"
FILE_USERS = "data/users.csv"
CHAMPS_ADMINS = ['id', 'login', 'password_hash', 'nom', 'prenom', 'role', 'site']
CHAMPS_USERS = ['id', 'login', 'password_hash', 'nom', 'prenom', 'role', 'site']

def generer_login(nom, prenom):
    """Génère le login : 1ère lettre prénom + nom."""
    if not nom or not prenom: return "inconnu"
    return f"{prenom[0].lower()}{nom.lower().replace(' ', '')}"

def verifier_droit_zone(current_user, cible_site):
    """
    Renvoie True si l'utilisateur a le droit d'agir sur ce site.
    Règle : Super Admin (Paris) a accès partout. Admin local a accès à son site uniquement.
    """
    if current_user['role'] == 'SUPER_ADMIN':
        return True
    if current_user['site'] == cible_site:
        return True
    return False

def lister_personnel(current_user, type_cible="users"):
    """READ: Affiche la liste filtrée par zone (Users ou Admins)."""
    fichier = FILE_USERS if type_cible == "users" else FILE_ADMINS
    data = storage.charger_csv(fichier)
    
    label = "UTILISATEURS" if type_cible == "users" else "ADMINISTRATEURS"
    print(f"\n--- LISTE DES {label} ({current_user['site'] if current_user['role'] != 'SUPER_ADMIN' else 'Global'}) ---")
    print(f"{'ID':<5} {'Login':<15} {'Nom':<15} {'Prénom':<15} {'Site':<10}")
    print("-" * 60)

    count = 0
    for p in data:
        # FILTRE : On ne montre que ce qui est dans la zone de droit
        if verifier_droit_zone(current_user, p['site']):
            print(f"{p['id']:<5} {p['login']:<15} {p['nom']:<15} {p['prenom']:<15} {p['site']:<10}")
            count += 1
    
    if count == 0:
        print(f"Aucun {type_cible[:-1]} trouvé dans votre zone.")

def ajouter_personne(current_user, type_cible="users"):
    """CREATE: Crée une personne (User ou Admin), forcée dans la zone de l'admin."""
    if current_user['role'] == 'USER':
        print("⛔ Action non autorisée.")
        return

    # Note : On autorise maintenant les ADMINS à créer d'autres ADMINS (sur leur site)
    
    print(f"\n--- AJOUTER UN {type_cible[:-1].upper()} ---")
    nom = input("Nom : ").strip()
    prenom = input("Prénom : ").strip()
    
    # LOGIQUE SITE :
    if current_user['role'] == 'SUPER_ADMIN':
        # Le Super Admin choisit librement le site
        site = input("Affecter au site (Paris, Marseille, Rennes, Grenoble) : ").strip()
    else:
        # L'Admin Local (Marseille) est FORCÉ à son site (Marseille)
        site = current_user['site']
        print(f"📍 Création automatique sur votre site de gestion : {site}")

    login = generer_login(nom, prenom)
    pwd_clair = auth.generer_mot_de_passe_aleatoire()
    pwd_hash = auth.hasher_mdp(pwd_clair)
    
    # Gestion ID
    fichier = FILE_USERS if type_cible == "users" else FILE_ADMINS
    champs = CHAMPS_USERS if type_cible == "users" else CHAMPS_ADMINS
    data = storage.charger_csv(fichier)
    new_id = len(data) + 1 

    # Définition du rôle
    role_assigne = 'USER'
    if type_cible == 'admins':
        if site == 'Paris' and current_user['role'] == 'SUPER_ADMIN':
             role_assigne = 'SUPER_ADMIN' # Seul un super admin peut en créer un autre
        else:
             role_assigne = 'ADMIN'

    nouvelle_personne = {
        'id': new_id, 'login': login, 'password_hash': pwd_hash,
        'nom': nom, 'prenom': prenom, 
        'role': role_assigne,
        'site': site
    }

    storage.ajouter_ligne_csv(fichier, nouvelle_personne, champs)
    print(f"✅ {type_cible[:-1].capitalize()} créé avec succès !")
    print(f"   Login : {login}")
    print(f"   Mdp   : {pwd_clair}")

def modifier_personne(current_user, type_cible="users"):
    """UPDATE: Modifie une personne de sa zone."""
    if current_user['role'] == 'USER': return

    lister_personnel(current_user, type_cible)
    id_modif = input("\nID à modifier : ").strip()
    
    fichier = FILE_USERS if type_cible == "users" else FILE_ADMINS
    champs = CHAMPS_USERS if type_cible == "users" else CHAMPS_ADMINS
    data = storage.charger_csv(fichier)
    
    trouve = False
    for p in data:
        if str(p['id']) == id_modif:
            # SÉCURITÉ : Vérifier que la cible est dans ma zone
            if not verifier_droit_zone(current_user, p['site']):
                print(f"⛔ Droit refusé sur le site {p['site']}.")
                return
            
            # SÉCURITÉ : Un Admin local ne peut pas modifier le Super Admin (même s'il le voit)
            if p['role'] == 'SUPER_ADMIN' and current_user['role'] != 'SUPER_ADMIN':
                print("⛔ Vous ne pouvez pas modifier le Super Admin.")
                return

            print(f"Modification de {p['login']} ({p['site']})")
            nouveau_nom = input(f"Nouveau nom ({p['nom']}) : ").strip()
            nouveau_prenom = input(f"Nouveau prénom ({p['prenom']}) : ").strip()
            
            if nouveau_nom: p['nom'] = nouveau_nom
            if nouveau_prenom: p['prenom'] = nouveau_prenom
            
            trouve = True
            break
    
    if trouve:
        storage.sauvegarder_csv(fichier, data, champs)
        print("✅ Modification enregistrée.")
    else:
        print("❌ ID introuvable dans votre zone.")

def supprimer_personne(current_user, type_cible="users"):
    """DELETE: Supprime une personne de sa zone."""
    if current_user['role'] == 'USER': return

    lister_personnel(current_user, type_cible)
    id_suppr = input("\nID à supprimer : ").strip()
    
    fichier = FILE_USERS if type_cible == "users" else FILE_ADMINS
    champs = CHAMPS_USERS if type_cible == "users" else CHAMPS_ADMINS
    data = storage.charger_csv(fichier)
    nouvelle_liste = []
    
    supprime = False
    for p in data:
        if str(p['id']) == id_suppr:
            # SÉCURITÉ : Vérifier zone
            if verifier_droit_zone(current_user, p['site']):
                # SÉCURITÉ : Protection anti-suicide (ne pas se supprimer soi-même)
                if p['login'] == current_user['login']:
                    print("⛔ Vous ne pouvez pas supprimer votre propre compte.")
                    nouvelle_liste.append(p)
                    continue

                # SÉCURITÉ : Protection Super Admin
                if p['role'] == 'SUPER_ADMIN' and current_user['role'] != 'SUPER_ADMIN':
                    print("⛔ Vous ne pouvez pas supprimer le Super Admin.")
                    nouvelle_liste.append(p)
                    continue

                print(f"🗑  Suppression de {p['login']} ({p['site']})...")
                supprime = True
            else:
                print(f"⛔ INTERDIT : Hors de votre zone ({p['site']}).")
                nouvelle_liste.append(p)
        else:
            nouvelle_liste.append(p)

    if supprime:
        storage.sauvegarder_csv(fichier, nouvelle_liste, champs)
        print("✅ Suppression effectuée.")
    else:
        print("❌ Aucune suppression (ID inconnu ou droits insuffisants).")