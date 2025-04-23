import json
import hashlib
from generate_block import create_genesis_block, create_block, load_matches_from_csv

# Funktion för att hämta blockchain från en fil
def get_blockchain():
    try:
        with open("blockchain.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Funktion för att spara blockchain till en fil
def save_blockchain(blockchain):
    with open("blockchain.json", "w") as f:
        json.dump(blockchain, f)

# Lägg till ett block i blockchain
def add_to_blockchain():
    blockchain = get_blockchain()

    # Om blockchain är tom, skapa genesis block
    if len(blockchain) == 0:
        blockchain.append(create_genesis_block())

    # Läsa in matchdata från CSV
    matches = load_matches_from_csv()

    # Få den senaste blockets hash
    previous_hash = blockchain[-1]["hash"]

    # Skapa ett nytt block och lägg till matchdata
    new_block = create_block(previous_hash, matches)

    # Lägg till blocket i blockchainen
    blockchain.append(new_block)

    # Spara den uppdaterade blockchainen
    save_blockchain(blockchain)
