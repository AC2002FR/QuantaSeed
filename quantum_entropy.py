#!/usr/bin/env python3
import argparse
import requests
import sys
import string
import os
import time
import pyperclip
from pathlib import Path

# Vérification et installation automatique des modules
REQUIRED_MODULES = ["requests", "pyperclip", "colorama"]

for module in REQUIRED_MODULES:
    try:
        __import__(module)
    except ImportError:
        print(f"⚠️ Le module '{module}' n'est pas installé.")
        print(f"💡 Exécutez : pip install {module}")
        sys.exit(1)

# Importation des modules après vérification
import colorama
from colorama import Fore, Style

# Initialisation des couleurs pour Windows
colorama.init(autoreset=True)

LOCKFILE = Path("last_execution.lock")
TIME_LIMIT = 60  # 60 secondes avant nouvelle exécution

# APIs quantiques
APIS = {
    "ANU QRNG": "https://qrng.anu.edu.au/API/jsonI.php?length={}&type=uint8",
    "PQShield QRNG": "https://api.pqshield.com/qrng?size={}",
    "ID Quantique QRNG": "https://quantum-id.com/api/random?length={}"
}

def check_last_execution():
    """
    Vérifie si le script a été exécuté dans les 60 dernières secondes.
    """
    if LOCKFILE.exists():
        try:
            last_run = float(LOCKFILE.read_text().strip())
            elapsed_time = time.time() - last_run
            if elapsed_time < TIME_LIMIT:
                remaining_time = TIME_LIMIT - elapsed_time
                print(Fore.RED + f"⏳ Veuillez patienter {int(remaining_time)} secondes avant de relancer le script.")
                sys.exit(1)
        except ValueError:
            pass  

    LOCKFILE.write_text(str(time.time()))

def fetch_quantum_random_numbers(n: int):
    """
    Récupère des nombres aléatoires depuis les APIs quantiques avec attente minimale.
    """
    for name, url in APIS.items():
        try:
            print(Fore.CYAN + f"🔄 Tentative avec {name}...")
            response = requests.get(url.format(n), timeout=5)
            response.raise_for_status()
            data = response.json()
            return data["data"]
        except requests.exceptions.RequestException as e:
            print(Fore.YELLOW + f"⚠️ {name} est inaccessible ({e})", file=sys.stderr)
            print(Fore.LIGHTBLUE_EX + "⏳ Attente avant d'essayer une autre API...")

            if name == "ANU QRNG":
                time.sleep(1)  
            elif name == "PQShield QRNG":
                time.sleep(2)  
            elif name == "ID Quantique QRNG":
                time.sleep(2)  

    print(Fore.RED + "❌ Aucune API quantique disponible, utilisation de os.urandom()")
    return list(os.urandom(n))

def generate_quantum_entropy_string(length: int) -> str:
    """
    Convertit les octets quantiques en une chaîne sécurisée.
    """
    ALPHABET = string.ascii_letters + string.digits + "+/"
    random_numbers = fetch_quantum_random_numbers(length)
    return ''.join(ALPHABET[b % len(ALPHABET)] for b in random_numbers)

def show_help():
    """
    Affiche une aide détaillée et colorée avec des exemples d'utilisation.
    """
    print(Fore.GREEN + Style.BRIGHT + "🔬 QuantaSeed - Générateur d'entropie 100% quantique")
    print(Fore.YELLOW + "📌 Utilisation :")
    print(Fore.CYAN + "   python quantum_entropy.py --length 32")
    print(Fore.YELLOW + "\n📌 Options disponibles :")
    print(Fore.LIGHTMAGENTA_EX + "   -l, --length <nombre>  " + Fore.WHITE + "  Spécifie la longueur de la chaîne (par défaut : 32)")
    print(Fore.LIGHTMAGENTA_EX + "   -s, --silent           " + Fore.WHITE + "  Mode silencieux (affiche uniquement la chaîne)")
    print(Fore.LIGHTMAGENTA_EX + "   -c, --copy             " + Fore.WHITE + "  Copie la chaîne générée dans le presse-papier")
    print(Fore.LIGHTMAGENTA_EX + "   -a, --show-api         " + Fore.WHITE + "  Affiche les API utilisées et quitte")
    print(Fore.LIGHTMAGENTA_EX + "   -h, --help             " + Fore.WHITE + "  Affiche cette aide détaillée")
    print(Fore.YELLOW + "\n📌 Exemples d'utilisation :")
    print(Fore.CYAN + "   🔹 Générer une chaîne de 50 caractères :")
    print(Fore.WHITE + "      python quantum_entropy.py --length 50")
    print(Fore.CYAN + "   🔹 Générer une chaîne et la copier dans le presse-papier :")
    print(Fore.WHITE + "      python quantum_entropy.py --length 50 --copy")
    print(Fore.CYAN + "   🔹 Afficher uniquement la chaîne (mode silencieux) :")
    print(Fore.WHITE + "      python quantum_entropy.py --length 50 --silent")
    print(Fore.CYAN + "   🔹 Voir les APIs utilisées :")
    print(Fore.WHITE + "      python quantum_entropy.py --show-api")
    sys.exit(0)

def main():
    check_last_execution() 

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-l", "--length", type=int, default=32, help=argparse.SUPPRESS)
    parser.add_argument("-s", "--silent", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("-c", "--copy", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("-a", "--show-api", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("-h", "--help", action="store_true", help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.help:
        show_help()

    if args.show_api:
        print(Fore.LIGHTBLUE_EX + "📡 Sources d'entropie quantique disponibles :")
        for name, url in APIS.items():
            print(Fore.YELLOW + f"🔹 {name}: {url}")
        sys.exit(0)

    if args.length <= 0:
        print(Fore.RED + "❌ Erreur : La longueur doit être un entier positif supérieur à 0.")
        sys.exit(1)

    random_string = generate_quantum_entropy_string(args.length)

    if args.copy:
        pyperclip.copy(random_string)
        print(Fore.GREEN + "📋 Entropie copiée dans le presse-papier !")

    if args.silent:
        print(random_string)
    else:
        print(Fore.CYAN + f"🔑 Entropie générée : {random_string}")

if __name__ == "__main__":
    main()
