import storage
# import users
# import admins
# import auth


def menu_principal():
    """Affiche le menu principal."""
    print("""
========================
  Ges_Users_AH - Menu
========================
1. Connexion administrateur
2. Quitter
""")


def main():
    """
    Point d'entrée du programme :
    - initialise le stockage
    - charge users et admins
    - affiche le menu principal en boucle
    """
    storage.init_storage()

    users_list = storage.load_users()
    admins_list = storage.load_admins()

    while True:
        menu_principal()
        choix = input("Votre choix : ")

        if choix == "1":
            # TODO : appeler auth.login_admin(admins_list)
            # puis afficher un menu administrateur.
            print("Connexion administrateur : à implémenter (Dev2 + Dev3).")
            # Exemple de debug si besoin :
            # print("Admins chargés :", admins_list)
        elif choix == "2":
            print("Au revoir.")
            break
        else:
            print("Choix invalide, merci de réessayer.")


if __name__ == "__main__":
    main()
