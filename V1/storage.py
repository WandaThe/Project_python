import csv
import os

def charger_csv(chemin_fichier):
   """Lit un fichier CSV et retourne une liste de dictionnaires."""
   data = []
   if not os.path.exists(chemin_fichier):
       return data
   
   try:
       with open(chemin_fichier, mode='r', encoding='utf-8', newline='') as csvfile:
           reader = csv.DictReader(csvfile)
           for row in reader:
               data.append(row)
   except Exception as e:
       print(f"Erreur lecture {chemin_fichier}: {e}")
   return data

def sauvegarder_csv(chemin_fichier, data, fieldnames):
   """Écrase le fichier CSV avec les nouvelles données."""
   try:
       with open(chemin_fichier, mode='w', encoding='utf-8', newline='') as csvfile:
           writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
           writer.writeheader()
           writer.writerows(data)
   except Exception as e:
       print(f"Erreur écriture {chemin_fichier}: {e}")

def ajouter_ligne_csv(chemin_fichier, ligne_dict, fieldnames):
   """Ajoute une seule ligne à la fin du fichier (append)."""
   fichier_existe = os.path.exists(chemin_fichier)
   try:
       with open(chemin_fichier, mode='a', encoding='utf-8', newline='') as csvfile:
           writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
           if not fichier_existe:
               writer.writeheader()
           writer.writerow(ligne_dict)
   except Exception as e:
       print(f"Erreur ajout {chemin_fichier}: {e}")

