import storage
#import users                 # Dev1
import users_admins as admins  # Dev2 (fichier users_admins.py)
import auth                  # Dev2


def menu_principal():
    """Affiche le menu principal."""
    print("""
========================
  Ges_Users_AH - Menu
========================
1. Connexion administrateur
2. Quitter
""")


def menu_gestion_utilisateurs(users_list):
    """
    Menu de gestion des utilisateurs (partie Dev1).
    users_list : liste de dictionnaires représentant les utilisateurs.
    Dev1 doit fournir dans users.py :
      - creer_utilisateur(users_list)
      - modifier_utilisateur(users_list)
      - supprimer_utilisateur(users_list)
      - rechercher_utilisateur(users_list)
      - lister_utilisateurs(users_list)
    """
    while True:
        print("""
----- Gestion des utilisateurs -----
1. Créer un utilisateur
2. Modifier un utilisateur
3. Supprimer un utilisateur
4. Rechercher un utilisateur
5. Lister tous les utilisateurs
6. Retour au menu administrateur
""")
        choix = input("Votre choix : ")

        if choix == "1":
            users.creer_utilisateur(users_list)
            storage.save_users(users_list)
        elif choix == "2":
            users.modifier_utilisateur(users_list)
            storage.save_users(users_list)
        elif choix == "3":
            users.supprimer_utilisateur(users_list)
            storage.save_users(users_list)
        elif choix == "4":
            users.rechercher_utilisateur(users_list)
        elif choix == "5":
            users.lister_utilisateurs(users_list)
        elif choix == "6":
            break
        else:
            print("Choix invalide, merci de réessayer.")


def menu_gestion_admins(admin_connecte):
    """
    Menu de gestion des administrateurs (partie Dev2).
    On s'appuie sur les fonctions de users_admins.py :
      - lister_personnel(current_user, type_cible="admins")
      - ajouter_personne(current_user, type_cible="admins")
      - modifier_personne(current_user, type_cible="admins")
      - supprimer_personne(current_user, type_cible="admins")
    """
    while True:
        print("""
----- Gestion des administrateurs -----
1. Lister les administrateurs
2. Créer un administrateur
3. Modifier un administrateur
4. Supprimer un administrateur
5. Retour au menu administrateur
""")
        choix = input("Votre choix : ")

        if choix == "1":
            admins.lister_personnel(admin_connecte, type_cible="admins")
        elif choix == "2":
            admins.ajouter_personne(admin_connecte, type_cible="admins")
        elif choix == "3":
            admins.modifier_personne(admin_connecte, type_cible="admins")
        elif choix == "4":
            admins.supprimer_personne(admin_connecte, type_cible="admins")
        elif choix == "5":
            break
        else:
            print("Choix invalide, merci de réessayer.")


def menu_admin_connecte(admin_connecte, users_list):
    """
    Menu affiché après la connexion d'un administrateur.
    admin_connecte : dict représentant l'admin connecté.
    users_list     : liste des utilisateurs (list[dict]).
    """
    while True:
        print("""
=============================
  Menu Administrateur
=============================
1. Gérer les utilisateurs
2. Gérer les administrateurs
3. Déconnexion
""")
        choix = input("Votre choix : ")

        if choix == "1":
            menu_gestion_utilisateurs(users_list)
        elif choix == "2":
            menu_gestion_admins(admin_connecte)
        elif choix == "3":
            print("Déconnexion...")
            break
        else:
            print("Choix invalide, merci de réessayer.")


def main():
    """
    Point d'entrée du programme.
    - Initialisation du stockage
    - Chargement des utilisateurs
    - Connexion admin + menus.
    """
    storage.init_storage()

    # Les utilisateurs sont chargés une fois et gérés en mémoire par Dev1
    users_list = storage.load_users()

    while True:
        menu_principal()
        choix = input("Votre choix : ")

        if choix == "1":
            # Dev2 doit implémenter auth.login_admin()
            # -> lit admins.csv (via storage.charger_csv) et renvoie un dict admin ou None.
            admin_connecte = auth.login_admin()

            if admin_connecte is not None:
                print("Connexion réussie. Bonjour",
                      admin_connecte.get("prenom", ""),
                      admin_connecte.get("nom", ""))
                menu_admin_connecte(admin_connecte, users_list)
            else:
                print("Échec de la connexion administrateur.")
        elif choix == "2":
            print("Au revoir.")
            break
        else:
            print("Choix invalide, merci de réessayer.")


if __name__ == "__main__":
    main()
