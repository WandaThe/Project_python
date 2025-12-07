import fonctions as f

def menu_principal(user):
    while True:
        f.effacer_ecran()
        role = user['role']
        print(f"=== AMERICAN HOSPITAL ===")
        print(f" {user['login']} | {role} | {user['site']}")
        print("-" * 30)
        
        print("1. [R] Lister Utilisateurs")
        if role in ['ADMIN', 'SUPER_ADMIN']:
            print("2. [C] Créer Utilisateur")
            print("3. [U] Modifier Utilisateur")
            print("4. [D] Supprimer Utilisateur")
            
            print("\n--- EQUIPE ADMIN ---")
            print("5. [R] Lister Admins")
            print("6. [C] Créer Admin")
            print("7. [D] Supprimer Admin")

        print("\nQ. Quitter")
        choix = input("Action : ").upper()

        if choix == '1': f.lister_personnel(user, "users")
        elif choix == '2' and role != 'USER': f.ajouter_personne(user, "users")
        elif choix == '3' and role != 'USER': f.modifier_personne(user, "users")
        elif choix == '4' and role != 'USER': f.supprimer_personne(user, "users")
        elif choix == '5' and role != 'USER': f.lister_personnel(user, "admins")
        elif choix == '6' and role != 'USER': f.ajouter_personne(user, "admins")
        elif choix == '7' and role != 'USER': f.supprimer_personne(user, "admins")
        elif choix == 'Q': break
        
        f.pause()

if __name__ == "__main__":
    session = f.login_systeme()
    if session:
        menu_principal(session)
