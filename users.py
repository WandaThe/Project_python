def creer_login(prenom, nom)  ### permet de creer le login en utilisant la premiere lettre du prenom + le nom
login = prenom[0].lower() + nom.lower()
return login ### On prend la premiere lettre du prenom puis on ajoute le nom

def champs_valider(prenom, nom, profil): ### Permet de valider les champs d'un utlisateur
if prenom == "" or nom == "":
    print ("Echouer : Ces champs ne peuvent pas etre vides")
    return False ### Cela permet de verifier que le champ ne soit pas vide 

    profils_valides = ["medecin" , "infirmier" . "autre"]
    if profil.lower() not in profils_valides:
        print("Le Profil doit etre infirmier, medecin ou autre.")
        return False

    return True ### Cela permet de verifier si le profil est valide 

def ajouter_user(liste_users, generer_mdp_fonction, hasher_mdp_fonction, date_creatiom)
print("\n Ajouter un nouvel utilisteur")
prenom = input("Prenom : ")
nom = input("Nom : ")
profil = input("Profil (medecin/infirmier/autre) : ") ### Cette fonction permet d'ajouter un nouvel utilisateur

if not champs_valider(prenom, nom, profil):
    return ### Cette fonction permet de valider les champs

    login = creer_login(prenom, nom) ### Permet de creer le login

    for user in liste_users:
        if user['login'] == login:
            print("Un utilisateur avec ce login est deja existant, merci de reessayer")
            return 

    mdp_generer = generer_mdp_fonction()
    print("Voici le mot de passe generer : " + mdp_generer) ### Cela permet de generer un mot de passe aleatoire

    mdp_hash = hasher_mdp_fonction(mdp_generer) ### Permet de hasher le mot de passe generer

    user = {
        "nom": nom,
        "prenom": prenom, 
        "login": login,
        "mdp": mdp_hash
        "profil": profil,
        "date de creation": date_creatiom,
    } ### Information sur l'utilisateur

    liste_users.append(user)
    print("Utilisateur" + login + "L'utilisateur a ete cree avec succes.")

def afficher_users(liste_users):
    print("\n Voici la liste des utilisateurs ")
    if len(liste_users) == 0:
        print("Il n'y a aucun utilisateur qui est enregistre.")
        else:
            for i in range(len(liste_users)):
                user = liste_users[i]
                print(str(i+1) + ". " + user['prenom'] + " " + user['nom'] + " - Login: " + user['login'] + " - Profil: " + user['profil'])
### Permet d'afficher tous les utilisateurs

def rechercher_user(liste_users):
    print("\n Recherche un utilisateur ")
    login_recherche = input("Ecrivez un user que vous voulez chercher : ") ### Cette fonction permet de rechercher un utlisateur en particulier
    trouve = False
    for user in liste_users:
        if user['login'] == login_recherche:
            print("\n L'utilisateur a ete trouve :")
            print("Nom: " + user['prenom'] + " " + user['nom'])
            print("Login: " + user['login'])
            print("Profil: " + user['profil'])
            print("Date creation: " + user['date_creation'])
            trouve = True
            break
        if not trouve:
            print("L'utilisateur na pas ete trouve.") ### Cette fonction permet de recherche un utilisateur en particulier en ecrivant sont login nom prenom etc

            













