import hashlib
import json
import os
from time import time

BLOCKCHAIN_FILE = "blockchain.json"

def hash_block(block):
    """Beräknar hash för ett block"""
    return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()


def load_blockchain():
    """Laddar blockchain från fil"""
    if os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    return []


def save_blockchain(blockchain):
    """Sparar blockchain till fil"""
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(blockchain, f, indent=2)


def create_new_block(winner, loser, result):
    """Skapar ett nytt block vid varje vinst"""
    transaction = {
        "from": winner,
        "to": loser,
        "amount": 1,  # En enhet per vinst, kan justeras
        "timestamp": time(),
        "result": result
    }

    # Hämta senaste blocket från blockchain
    blockchain = load_blockchain()
    previous_block = blockchain[-1] if blockchain else None

    # Skapa det nya blocket
    block = {
        "timestamp": time(),
        "previous_hash": previous_block['hash'] if previous_block else None,
        "transactions": [transaction],
    }

    # Beräkna och tilldela hash för blocket
    block['hash'] = hash_block(block)
    return block


def add_block_to_chain(block):
    """Lägger till blocket i blockchain och sparar"""
    blockchain = load_blockchain()
    blockchain.append(block)
    save_blockchain(blockchain)


def create_new_block_for_victory(winner, loser, result):
    """Hanterar skapandet och lagring av ett nytt block för en vinst"""
    new_block = create_new_block(winner, loser, result)
    add_block_to_chain(new_block)
    print(f"Game won! New block added to the blockchain: {winner} vs {loser}, Result: {result}")
