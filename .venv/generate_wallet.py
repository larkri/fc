import json
import os
from ecdsa import SigningKey, SECP256k1

WALLET_FILE = "wallets.json"

def generate_wallet():
    # Generera en privat nyckel och en offentlig nyckel
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.verifying_key

    # Skapa plånboken med en initial balans
    wallet = {
        "private_key": private_key.to_string().hex(),
        "public_key": public_key.to_string().hex(),
        "balance": 100  # Initial saldo för genesis-blocket
    }

    # Läs nuvarande plånböcker om filen finns
    if os.path.exists(WALLET_FILE):
        with open(WALLET_FILE, "r") as f:
            wallets = json.load(f)
    else:
        wallets = []

    # Lägg till den nya plånboken
    wallets.append(wallet)

    # Spara alla plånböcker till wallets.json
    with open(WALLET_FILE, "w") as f:
        json.dump(wallets, f, indent=4)

    print("Ny plånbok skapad:")
    print(json.dumps(wallet, indent=4))

if __name__ == "__main__":
    generate_wallet()
