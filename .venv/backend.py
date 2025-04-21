from flask import Flask, render_template, request, jsonify
import json
import time
import hashlib
import os

app = Flask(__name__)

MEMPOOL_FILE = "mempool.json"

# Funktion för att hämta alla plånböcker från wallets.json
def get_wallets():
    try:
        with open('wallets.json', 'r') as file:
            wallets = json.load(file)
        return wallets
    except Exception as e:
        print(f"Fel vid läsning av wallets.json: {e}")
        return []

# Funktion för att hämta saldo för en viss public_key
def get_balance(public_key):
    wallets = get_wallets()
    for wallet in wallets:
        if wallet['public_key'] == public_key:
            return wallet['balance']
    return None

# Funktion för att spara tillbaka plånböckerna till wallets.json
def save_wallets(wallets):
    try:
        with open('wallets.json', 'w') as file:
            json.dump(wallets, file, indent=4)
    except Exception as e:
        print(f"Fel vid skrivning av wallets.json: {e}")

# Funktion för att läsa in blockchain från blockchain.json
def get_blockchain():
    try:
        with open('blockchain.json', 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Fel vid läsning av blockchain.json: {e}")
        return []

# Funktion för att spara blockchain till blockchain.json
def save_blockchain(blockchain):
    try:
        with open('blockchain.json', 'w') as file:
            json.dump(blockchain, file, indent=4)
    except Exception as e:
        print(f"Fel vid skrivning till blockchain.json: {e}")

# Funktion för att läsa och spara till mempool.json
def load_mempool():
    if os.path.exists(MEMPOOL_FILE):
        with open(MEMPOOL_FILE, 'r') as file:
            return json.load(file)
    return []

def save_mempool(mempool):
    with open(MEMPOOL_FILE, "w") as f:
        json.dump(mempool, f, indent=2)

# Funktion för att skapa en ny transaktion och lägga till den i mempoolen
def create_transaction_block(from_key, to_key, amount):
    mempool = load_mempool()

    # Skapa nytt transaktionsobjekt
    new_transaction = {
        "from": from_key,
        "to": to_key,
        "amount": amount,
        "timestamp": time.time(),
        "hash": hashlib.sha256(f"{from_key}{to_key}{amount}{time.time()}".encode()).hexdigest()
    }

    mempool.append(new_transaction)
    save_mempool(mempool)

# Rutt för att visa plånbokens saldo
@app.route('/wallet', methods=['GET'])
def wallet():
    public_key = request.args.get('public_key')  # Hämta public_key från URL-parametrarna
    balance = None
    if public_key:
        balance = get_balance(public_key)  # Hämta saldo för den angivna public_key
    return render_template("wallet.html", balance=balance, public_key=public_key)

# Rutt för att skicka tokens
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        from_key = request.form.get('from')
        private_key = request.form.get('private')
        to_key = request.form.get('to')
        amount = float(request.form.get('amount'))

        # Uppdatera plånböcker (hämta plånböcker från wallets.json)
        wallets = get_wallets()
        from_wallet = next((w for w in wallets if w['public_key'] == from_key), None)
        to_wallet = next((w for w in wallets if w['public_key'] == to_key), None)

        # Kontrollera om plånböcker finns och om avsändaren har tillräckligt med saldo
        if from_wallet and to_wallet and from_wallet['balance'] >= amount:
            from_wallet['balance'] -= amount
            to_wallet['balance'] += amount

            # Spara nya saldon i wallets.json
            save_wallets(wallets)

            # Skapa och lägg till transaktionen i mempoolen
            create_transaction_block(from_key, to_key, amount)

            return render_template('send.html', success=True)
        else:
            return render_template('send.html', error="Transaktion misslyckades")

    return render_template('send.html')

if __name__ == '__main__':
    app.run(debug=True)
