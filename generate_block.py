import time
import hashlib
import json
import csv


# Funktion för att skapa genesis blocket
def create_genesis_block():
    """
    Skapar genesis blocket, dvs. det första blocket i blockchain.
    """
    genesis_block = {
        "timestamp": time.time(),
        "previous_hash": "0",  # Ingen tidigare hash för det första blocket
        "matches": [],  # Ingen matchdata i genesis block
        "hash": hashlib.sha256(f"0{str([])}{time.time()}".encode()).hexdigest()
    }
    return genesis_block


# Funktion för att skapa ett nytt block
def create_block(previous_hash, matches):
    """
    Skapar ett nytt block med matchdata och länkar det till det föregående blocket.
    """
    block = {
        "timestamp": time.time(),
        "previous_hash": previous_hash,
        "matches": matches,  # Matchdata som ska ingå i blocket
        "hash": hashlib.sha256(f"{previous_hash}{str(matches)}{time.time()}".encode()).hexdigest()
    }
    return block


# Läsa matchdata från en CSV-fil
def load_matches_from_csv(csv_file="matches.csv"):
    matches = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            match = {
                "viewable": row['Viewable'],
                "white": row['White'],
                "black": row['Black'],
                "setup": row['Setup'],
                "start_time": row['Start Time'],
                "type": row['Type'],
                "result": row['Result']
            }
            matches.append(match)
    return matches


# Ladda blockchain från fil
def load_blockchain_from_file(filename="blockchain.json"):
    try:
        with open(filename, "r") as f:
            blockchain = json.load(f)
            return blockchain
    except (FileNotFoundError, json.JSONDecodeError):
        # Om filen inte finns eller är tom, returnera en tom lista
        return []


# Spara blockchain till fil
def save_blockchain_to_file(blockchain, filename="blockchain.json"):
    with open(filename, "w") as f:
        json.dump(blockchain, f, indent=4)


# Main funktion för att generera blockkedjan
def main():
    # Försök att ladda existerande blockkedja från filen
    blockchain = load_blockchain_from_file()

    # Om blockkedjan är tom (första gången körs), skapa Genesis Block
    if len(blockchain) == 0:
        genesis_block = create_genesis_block()
        blockchain.append(genesis_block)
        print("Genesis block skapades och lades till i blockkedjan.")

    # Ladda matchdata från CSV
    matches = load_matches_from_csv()

    # Skapa ett nytt block och lägg till det i blockkedjan
    if blockchain:
        previous_block = blockchain[-1]
        new_block = create_block(previous_block['hash'], matches)
        blockchain.append(new_block)
        print("Nytt block skapades och lades till i blockkedjan.")

    # Spara den uppdaterade blockkedjan till fil
    save_blockchain_to_file(blockchain)
    print("Blockkedjan har sparats till blockchain.json")


if __name__ == "__main__":
    main()
