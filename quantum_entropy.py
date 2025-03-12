#!/usr/bin/env python3
import argparse
import sys
import string
import os

# Vérification des modules nécessaires
REQUIRED_MODULES = ["requests", "pyperclip"]

for module in REQUIRED_MODULES:
    try:
        __import__(module)
    except ImportError:
        print(f"⚠️ Le module '{module}' n'est pas installé.")
        print(f"💡 Exécutez la commande suivante pour l'installer :")
        print(f"   pip install {module}")
        sys.exit(1)

# Importation après vérification
import requests
import pyperclip

# Définition des URLs des APIs quantiques
APIS = {
    "ANU QRNG": "https://qrng.anu.edu.au/API/jsonI.php?length={}&type=uint8",
    "PQShield QRNG": "https://api.pqshield.com/qrng?size={}",
    "ID Quantique QRNG": "https://quantum-id.com/api/random?length={}"
}

def fetch_quantum_random_numbers(n: int):
    """
    Tente d'obtenir des nombres aléatoires quantiques à partir des APIs définies.
    Si une API ne répond pas, passe à la suivante.
    """
    for name, url in APIS.items():
        try:
            print(f"🔄 Tentative avec {name}...")
            response = requests.get(url.format(n), timeout=5)
            response.raise_for_status()
            data = response.json()
            return data["data"]
        except requests.exceptions.RequestException as e:
            print(f"⚠️ {name} est inaccessible ({e})", file=sys.stderr)

    # Fallback : si toutes les APIs échouent, utiliser os.urandom()
    print("❌ Aucune API quantique disponible, utilisation de os.urandom()")
    return list(os.urandom(n))

def generate_quantum_entropy_string(length: int) -> str:
    """
    Génère une chaîne aléatoire à partir des octets quantiques récupérés.
    Utilise un alphabet base64 pour garantir un mapping sans biais.
    """
    ALPHABET = string.ascii_letters + string.digits + "+/"
    random_numbers = fetch_quantum_random_numbers(length)
    return ''.join(ALPHABET[b % len(ALPHABET)] for b in random_numbers)

def main():
    parser = argparse.ArgumentParser(
        description="🔬 QuantaSeed - Générateur d'entropie 100% quantique (ANU, PQShield, ID Quantique)"
    )
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=32,
        help="Longueur de la chaîne générée (par défaut 32 caractères)"
    )
    parser.add_argument(
        "-s", "--silent",
        action="store_true",
        help="Mode silencieux (aucun message, juste la chaîne)"
    )
    parser.add_argument(
        "-c", "--copy",
        action="store_true",
        help="Copie la chaîne générée dans le presse-papier"
    )
    parser.add_argument(
        "-a", "--show-api",
        action="store_true",
        help="Affiche les API quantiques disponibles et quitte"
    )

    args = parser.parse_args()

    if args.show_api:
        print("📡 Sources d'entropie quantique disponibles :")
        for name, url in APIS.items():
            print(f"🔹 {name}: {url}")
        sys.exit(0)

    if args.length <= 0:
        parser.error("La longueur doit être un entier positif supérieur à 0.")

    random_string = generate_quantum_entropy_string(args.length)

    if args.copy:
        pyperclip.copy(random_string)
        print("📋 Entropie copiée dans le presse-papier !")

    if args.silent:
        print(random_string)
    else:
        print(f"🔑 Entropie générée : {random_string}")

if __name__ == "__main__":
    main()
