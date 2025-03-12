#!/usr/bin/env python3
import argparse
import requests
import sys
import string

QRNG_API_URL = "https://qrng.ethz.ch/api/randbytes"

def fetch_quantum_random_numbers(n: int):
    """
    Récupère des nombres aléatoires issus d'un générateur quantique.
    Utilise l'API QRNG ETH Zürich, qui génère de l'entropie basée sur un phénomène quantique.
    """
    try:
        response = requests.get(QRNG_API_URL, params={"size": n}, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["data"]
    except requests.exceptions.RequestException as e:
        print(f"Erreur : Impossible de récupérer l'entropie quantique ({e})", file=sys.stderr)
        sys.exit(1)

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
        description="Générateur d'entropie quantique via QRNG ETH Zürich."
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
    print(random_string)

if __name__ == "__main__":
    main()
