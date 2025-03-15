#!/usr/bin/env python3
import argparse
import requests
import sys
import string
import os
import time
import pyperclip
import math
from collections import Counter
from pathlib import Path

# Vérification et installation automatique des modules
REQUIRED_MODULES = ["requests", "pyperclip", "colorama"]

for module in REQUIRED_MODULES:
    try:
        __import__(module)
    except ImportError:
        print(f"⚠️ Le module '{module}' n'est pas installé.")
        print(f"💡 Exécutez : pip install {module}\n")
        sys.exit(1)

# Importation après vérification
import colorama
from colorama import Fore, Style

# Initialisation des couleurs pour Windows
colorama.init(autoreset=True)

LOCKFILE = Path("last_execution_length.lock")
TIME_LIMIT = 90  # 90 secondes avant de pouvoir exécuter à nouveau --length
MAX_LENGTH = 1024  # Définir une longueur maximale raisonnable

# API QUANTIQUE UNIQUE UTILISÉE
ANU_QRNG_API = "https://qrng.anu.edu.au/API/jsonI.php?length={}&type=uint8"

def check_last_execution():
    """ Vérifie si le script a été exécuté avec `-l` ou `--length` dans les 90 dernières secondes. """
    if LOCKFILE.exists():
        try:
            last_run = float(LOCKFILE.read_text().strip())
            elapsed_time = time.time() - last_run
            if elapsed_time < TIME_LIMIT:
                remaining_time = TIME_LIMIT - elapsed_time
                print(Fore.RED + f"\n⏳ Veuillez patienter {int(remaining_time)} secondes avant de relancer --length.\n")
                sys.exit(1)
        except ValueError:
            pass  

def fetch_quantum_random_numbers(n: int):
    """ Récupère des nombres aléatoires depuis l'API ANU QRNG. """
    try:
        print(Fore.CYAN + f"\n🔄 Tentative avec ANU QRNG (length={n})...\n")
        response = requests.get(ANU_QRNG_API.format(n), timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["data"]
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"\n❌ Erreur : Impossible d'obtenir l'entropie quantique ({e})")
        sys.exit(1)

def generate_quantum_entropy_string(length: int) -> str:
    """ Convertit les octets quantiques en une chaîne sécurisée. """
    ALPHABET = string.ascii_letters + string.digits + "+/"
    random_numbers = fetch_quantum_random_numbers(length)
    return ''.join(ALPHABET[b % len(ALPHABET)] for b in random_numbers)

def calculate_entropy(data):
    """ Calcule l'entropie de Shannon d'une chaîne de caractères. """
    if not data:
        return 0

    frequency = Counter(data)
    length = len(data)

    entropy = -sum((freq / length) * math.log2(freq / length) for freq in frequency.values())
    return entropy

def validate_length(value):
    """ Vérifie si la longueur est bien un entier positif et dans la limite autorisée. """
    try:
        ivalue = int(value)
        if ivalue < 1 or ivalue > MAX_LENGTH:
            raise argparse.ArgumentTypeError(f"❌ --length doit être entre 1 et {MAX_LENGTH}.")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError("❌ --length doit être un nombre entier valide.")

def main():
    parser = argparse.ArgumentParser(description="QuantaSeed - Générateur d'entropie quantique")
    parser.add_argument("-l", "--length", type=validate_length, default=1024, help=f"🔒 Spécifie la longueur de la chaîne (1-{MAX_LENGTH}, défaut : 1024)")
    parser.add_argument("-s", "--silent", action="store_true", help="🔕 Mode silencieux (affiche uniquement la chaîne générée)")
    parser.add_argument("-c", "--copy", action="store_true", help="📋 Copie la chaîne générée dans le presse-papier")
    parser.add_argument("--entropy-metric", action="store_true", help="📊 Évalue la force de l'entropie")
    parser.add_argument("-a", "--show-api", action="store_true", help="📡 Affiche l'API quantique utilisée et quitte")
    parser.add_argument("--aide", action="store_true", help="🇫🇷 Affiche l'aide en français")

    args = parser.parse_args()

    if args.aide:
        print(Fore.GREEN + "🔬 QuantaSeed - Générateur d'entropie quantique")
        print(Fore.YELLOW + "📌 Utilisation :")
        print(Fore.CYAN + "   python quantaseed.py --length 1024")
        print(Fore.YELLOW + "\n📌 Options disponibles :")
        print(Fore.LIGHTMAGENTA_EX + "   -l, --length <nombre>  " + Fore.WHITE + "  Spécifie la longueur de la chaîne (par défaut : 1024)")
        print(Fore.LIGHTMAGENTA_EX + "   -s, --silent           " + Fore.WHITE + "  Mode silencieux (affiche uniquement la chaîne)")
        print(Fore.LIGHTMAGENTA_EX + "   -c, --copy             " + Fore.WHITE + "  Copie la chaîne générée dans le presse-papier")
        print(Fore.LIGHTMAGENTA_EX + "   --entropy-metric       " + Fore.WHITE + "  Affiche l'entropie de Shannon de la chaîne générée")
        print(Fore.LIGHTMAGENTA_EX + "   -a, --show-api         " + Fore.WHITE + "  Affiche l'API quantique utilisée et quitte")
        print(Fore.LIGHTMAGENTA_EX + "   --aide                 " + Fore.WHITE + "  Affiche cette aide en français")
        sys.exit(0)

    if args.show_api:
        print(Fore.LIGHTBLUE_EX + "\n📡 API d'entropie quantique utilisée :")
        print(Fore.YELLOW + f"🔹 ANU QRNG: {ANU_QRNG_API.format('<length>')}\n")
        sys.exit(0)

    if args.length:
        check_last_execution()
        LOCKFILE.write_text(str(time.time()))

    random_string = generate_quantum_entropy_string(args.length)

    if args.copy:
        pyperclip.copy(random_string)
        print(Fore.GREEN + "\n📋 Chaîne copiée dans le presse-papier !\n")

    if not args.silent:
        print(Fore.CYAN + f"\n🔑 Chaîne générée : {random_string}\n")

    if args.entropy_metric:
        entropy_value = calculate_entropy(random_string)
        print(Fore.YELLOW + f"\n📊 Entropie de Shannon : {entropy_value:.4f} bits par caractère\n")

if __name__ == "__main__":
    main()
