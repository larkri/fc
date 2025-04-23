import os
import hashlib
import json

# Funktion för att skapa en ny plånbok
def generate_wallet():
    private_key = os.urandom(32)  # Slumpmässig privat nyckel
    public_key = hashlib.sha256(private_key).hexdigest()  # Beräkna den offentliga nyckeln

    wallet = {
        "public_key": public_key,
        "private_key": private_key.hex(),
        "balance": 0  # Startsaldo sätts till 0
    }

    wallets = get_wallets()
    wallets.append(wallet)
    save_wallets(wallets)  # Spara den nya plånboken
    return wallet

# Hämta alla plånböcker från en lagrad fil
def get_wallets():
    try:
        with open("wallets.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Spara plånböcker till en fil
def save_wallets(wallets):
    with open("wallets.json", "w") as f:
        json.dump(wallets, f, indent=4)

# Testa funktionen genom att skapa en ny plånbok
if __name__ == "__main__":
    new_wallet = generate_wallet()
    print(f"Ny plånbok skapad: {new_wallet}")
