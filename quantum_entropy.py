#!/usr/bin/env python3
import argparse
import requests
import sys
import string
import random
import time

# Définition des URLs des APIs
APIS = {
    "ETH Zürich": "https://qrng.ethz.ch/api/randbytes",
    "ANU QRNG": "https://qrng.anu.edu.au/API/jsonI.php?length={}&type=uint8",
    "Random.org": "https://www.random.org/integers/?num={}&min=0&max=255&col=1&base=10&format=plain&rnd=new"
}

def fetch_quantum_random_numbers(n: int):
    """
    Essaie d'obtenir des nombres aléatoires à partir de plusieurs sources quantiques.
    Si une API ne répond pas, passe à la suivante.
    """
    for name, url in APIS.items():
        try:
            print(f"🔄 Tentative avec {name}...")
            if "ethz.ch" in url:
                response = requests.get(url, params={"size": n}, timeout=5)
                response.raise_for_status()
                data = response.json()
                return data["data"]
            elif "anu.edu.au" in url:
                response = requests.get(url.format(n), timeout=5)
                response.raise_for_status()
                data = response.json()
                return data["data"]
            elif "random.org" in url:
                response = requests.get(url.format(n), timeout=5)
                response.raise_for_status()
                return [int(x) for x in response.text.strip().split()]
        except requests.exceptions.RequestException as e:
            print(f"⚠️ {name} est inaccessible ({e})")

    # Si toutes les APIs échouent, générer une entropie locale (fallback)
    print("❌ Aucune API quantique disponible, utilisation de os.urandom()")
    return list(os.urandom(n))

def generate_quantum_entropy_string(length: int) -> str:
    """
    Génère une chaîne aléatoire à partir des octets quantiques.
    Utilise un alphabet en base64 pour un mapping sans biais.
    """
    ALPHABET = string.ascii_letters + string.digits + "+/"
    random_numbers = fetch_quantum_random_numbers(length)
    return ''.join(ALPHABET[b % len(ALPHABET)] for b in random_numbers)

def main():
    parser = argparse.ArgumentParser(
        description="Générateur d'entropie quantique via 3 sources de QRNG."
    )
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=32,
        help="Longueur de la chaîne générée (par défaut 32 caractères)"
    )
    args = parser.parse_args()

    if args.length <= 0:
        parser.error("La longueur doit être un entier positif supérieur à 0.")

    random_string = generate_quantum_entropy_string(args.length)
    print(f"🔑 Entropie générée : {random_string}")

if __name__ == "__main__":
    main()
