import hashlib
import json
from time import time
import os

BLOCKCHAIN_FILE = "blockchain.json"
WALLET_FILE = "wallets.json"


def hash_block(block):
    return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()


def create_genesis_block(receiver_public_key):
    # Skapa genesis-transaktionen med ett initialt saldo
    genesis_transaction = {
        "from": None,
        "to": receiver_public_key,
        "amount": 100,  # Startbelopp för mottagarens plånbok
        "timestamp": time()
    }

    # Skapa blocket
    block = {
        "timestamp": time(),
        "previous_hash": None,
        "transactions": [genesis_transaction],
    }

    # Beräkna och tilldela hash till blocket
    block['hash'] = hash_block(block)
    return block


def save_blockchain(blockchain):
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(blockchain, f, indent=2)


def get_public_key_from_wallet():
    # Läs plånböcker från wallets.json och returnera den första public_key
    with open(WALLET_FILE, "r") as f:
        wallets = json.load(f)
    return wallets[0]['public_key']  # Returnera public key från den första plånboken


def main():
    # Hämta public key från plånboken
    receiver_key = get_public_key_from_wallet()

    # Skapa genesis block
    genesis_block = create_genesis_block(receiver_key)

    # Spara blockkedjan
    save_blockchain([genesis_block])

    print("Genesis block skapat!")


if __name__ == "__main__":
    main()
