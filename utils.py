import os
import platform

def effacer_ecran():
    """Nettoie la console selon l'OS."""
    system_name = platform.system()
    if system_name == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def pause():
    """Met le script en pause."""
    input("\nAppuyez sur Entrée pour continuer...")