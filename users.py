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







