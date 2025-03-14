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

# Importation après vérification
import colorama
from colorama import Fore, Style

# Initialisation des couleurs pour Windows
colorama.init(autoreset=True)

LOCKFILE = Path("last_execution_length.lock")
TIME_LIMIT = 90  # 90 secondes avant de pouvoir exécuter à nouveau --length

# API QUANTIQUE UNIQUE UTILISÉE
ANU_QRNG_API = "https://qrng.anu.edu.au/API/jsonI.php?length={}&type=uint8"

def check_last_execution():
    """
    Vérifie si le script a été exécuté avec `-l` ou `--length` dans les 90 dernières secondes.
    """
    if LOCKFILE.exists():
        try:
            last_run = float(LOCKFILE.read_text().strip())
            elapsed_time = time.time() - last_run
            if elapsed_time < TIME_LIMIT:
                remaining_time = TIME_LIMIT - elapsed_time
                print(Fore.RED + f"⏳ Veuillez patienter {int(remaining_time)} secondes avant de relancer --length.")
                sys.exit(1)
        except ValueError:
            pass  

def fetch_quantum_random_numbers(n: int):
    """
    Récupère des nombres aléatoires depuis l'API ANU QRNG.
    """
    try:
        print(Fore.CYAN + f"🔄 Tentative avec ANU QRNG (length={n})...")
        response = requests.get(ANU_QRNG_API.format(n), timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["data"]
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"❌ Erreur : Impossible d'obtenir l'entropie quantique ({e})")
        sys.exit(1)

def generate_quantum_entropy_string(length: int) -> str:
    """
    Convertit les octets quantiques en une chaîne sécurisée.
    """
    ALPHABET = string.ascii_letters + string.digits + "+/"
    random_numbers = fetch_quantum_random_numbers(length)
    return ''.join(ALPHABET[b % len(ALPHABET)] for b in random_numbers)

def show_help():
    """
    Affiche l'aide en anglais.
    """
    print(Fore.GREEN + Style.BRIGHT + "🔬 QuantaSeed - True Quantum Entropy Generator")
    print(Fore.YELLOW + "📌 Usage:")
    print(Fore.CYAN + "   python quantum_entropy.py --length 32")
    print(Fore.YELLOW + "\n📌 Available options:")
    print(Fore.LIGHTMAGENTA_EX + "   -l, --length <number>  " + Fore.WHITE + "  Specify string length (default: 32)")
    print(Fore.LIGHTMAGENTA_EX + "   -s, --silent           " + Fore.WHITE + "  Silent mode (outputs only the string)")
    print(Fore.LIGHTMAGENTA_EX + "   -c, --copy             " + Fore.WHITE + "  Copies the generated string to clipboard")
    print(Fore.LIGHTMAGENTA_EX + "   -a, --show-api         " + Fore.WHITE + "  Shows the quantum API used and exits")
    print(Fore.LIGHTMAGENTA_EX + "   -h, --help             " + Fore.WHITE + "  Displays this help")
    print(Fore.LIGHTMAGENTA_EX + "   --aide              " + Fore.WHITE + "  Affiche l'aide en français")
    sys.exit(0)

def show_aide():
    """
    Affiche l'aide en français.
    """
    print(Fore.GREEN + Style.BRIGHT + "🔬 QuantaSeed - Générateur d'entropie quantique")
    print(Fore.YELLOW + "📌 Utilisation :")
    print(Fore.CYAN + "   python quantum_entropy.py --length 32")
    print(Fore.YELLOW + "\n📌 Options disponibles :")
    print(Fore.LIGHTMAGENTA_EX + "   -l, --length <nombre>  " + Fore.WHITE + "  Spécifie la longueur de la chaîne (par défaut : 32)")
    print(Fore.LIGHTMAGENTA_EX + "   -s, --silent           " + Fore.WHITE + "  Mode silencieux (affiche uniquement la chaîne)")
    print(Fore.LIGHTMAGENTA_EX + "   -c, --copy             " + Fore.WHITE + "  Copie la chaîne générée dans le presse-papier")
    print(Fore.LIGHTMAGENTA_EX + "   -a, --show-api         " + Fore.WHITE + "  Affiche l'API quantique utilisée et quitte")
    print(Fore.LIGHTMAGENTA_EX + "   -h, --help             " + Fore.WHITE + "  Affiche l'aide en anglais")
    print(Fore.LIGHTMAGENTA_EX + "   --aide              " + Fore.WHITE + "  Affiche cette aide en français")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-l", "--length", type=int, default=32)
    parser.add_argument("-s", "--silent", action="store_true")
    parser.add_argument("-c", "--copy", action="store_true")
    parser.add_argument("-a", "--show-api", action="store_true")
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("--aide", action="store_true")

    args = parser.parse_args()

    if args.help:
        show_help()
    if args.aide:
        show_aide()
    if args.show_api:
        print(Fore.LIGHTBLUE_EX + "📡 Quantum Entropy API used:")
        print(Fore.YELLOW + f"🔹 ANU QRNG: {ANU_QRNG_API.format('<length>')}")
        sys.exit(0)

    # Vérifier l'attente uniquement pour --length
    if args.length:
        check_last_execution()
        LOCKFILE.write_text(str(time.time()))

    random_string = generate_quantum_entropy_string(args.length)

    if args.copy:
        pyperclip.copy(random_string)
        print(Fore.GREEN + "📋 Entropy copied to clipboard!")

    print(Fore.CYAN + f"🔑 Generated Entropy: {random_string}")

if __name__ == "__main__":
    main()
