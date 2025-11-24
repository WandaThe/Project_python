import auth_pwd
import users_admins
import utils

def menu_principal(user):
    while True:
        utils.effacer_ecran()
        role = user['role']
        site = user['site']
        
        print(f"=== GESTION USERS - AMERICAN HOSPITAL ===")
        print(f"👤 {user['login']} | 🛡 {role} | 📍 {site}")
        print("-" * 40)
        
        # --- GESTION DES UTILISATEURS (USERS) ---
        print("--- GESTION DES PATIENTS/USERS ---")
        print("1. [R] Lister les utilisateurs")
        
        if role in ['ADMIN', 'SUPER_ADMIN']:
            print("2. [C] Créer un utilisateur")
            print("3. [U] Modifier un utilisateur")
            print("4. [D] Supprimer un utilisateur")
        
        # --- GESTION DES ADMINISTRATEURS (ADMINS) ---
        # Maintenant accessible aux Admins locaux pour gérer LEUR équipe locale
        if role in ['ADMIN', 'SUPER_ADMIN']:
            print("\n--- GESTION DE VOTRE ÉQUIPE ADMIN ---")
            print("5. [R] Lister les admins")
            print("6. [C] Créer un admin")
            print("7. [D] Supprimer un admin")
            # Note: Modifier un admin peut aussi être ajouté si besoin
        
        print("\nQ. Quitter")
        print("-" * 40)
        
        choix = input("Votre choix : ").upper()

        # Actions sur USERS
        if choix == '1':
            users_admins.lister_personnel(user, "users")
        elif choix == '2' and role in ['ADMIN', 'SUPER_ADMIN']:
            users_admins.ajouter_personne(user, "users")
        elif choix == '3' and role in ['ADMIN', 'SUPER_ADMIN']:
            users_admins.modifier_personne(user, "users")
        elif choix == '4' and role in ['ADMIN', 'SUPER_ADMIN']:
            users_admins.supprimer_personne(user, "users")
        
        # Actions sur ADMINS
        elif choix == '5' and role in ['ADMIN', 'SUPER_ADMIN']:
            users_admins.lister_personnel(user, "admins")
        elif choix == '6' and role in ['ADMIN', 'SUPER_ADMIN']:
            users_admins.ajouter_personne(user, "admins")
        elif choix == '7' and role in ['ADMIN', 'SUPER_ADMIN']:
            users_admins.supprimer_personne(user, "admins")
            
        elif choix == 'Q':
            print("Fermeture de la session.")
            break
        elif choix == "D":
           print("Déconnexion...")
           break
        else:
            print("Choix invalide.")
        
        utils.pause()

if __name__ == "__main__":
    session = auth_pwd.login_systeme()
    if session:
        menu_principal(session)

