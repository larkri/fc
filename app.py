import hashlib
import json
import time
import os
from flask import Flask, render_template, request
import threading

# Importera scraperfunktion
import kgsarchive

# Starta scraper i bakgrundstråd
scraper_thread = threading.Thread(target=kgsarchive.run_scraper, daemon=True)
scraper_thread.start()
print("kgsarchive.py körs som bakgrundstråd.")

app = Flask(__name__)

# Centralt filhanterings-utility
def load_json(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([], f)
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []

def save_json(filename, data):
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving {filename}: {e}")

# Wallet-funktioner
def get_wallets():
    return load_json("wallets.json")

def save_wallets(wallets):
    save_json("wallets.json", wallets)

def get_balance(public_key, wallets):
    for wallet in wallets:
        if wallet['public_key'] == public_key:
            return wallet.get('balance', 0)
    return None

def update_balance(public_key, new_balance, wallets):
    for wallet in wallets:
        if wallet['public_key'] == public_key:
            wallet['balance'] = new_balance
            return True
    return False

# Transaktioner
def create_transaction(from_public_key, to_public_key, amount):
    timestamp = time.time()
    tx_string = f"{from_public_key}{to_public_key}{amount}{timestamp}"
    tx_hash = hashlib.sha256(tx_string.encode()).hexdigest()
    return {
        "from": from_public_key,
        "to": to_public_key,
        "amount": amount,
        "timestamp": timestamp,
        "hash": tx_hash
    }

def add_to_mempool(transaction):
    mempool = load_json("mempool.json")
    mempool.append(transaction)
    save_json("mempool.json", mempool)

def is_valid_transaction(from_public_key, amount, wallets):
    balance = get_balance(from_public_key, wallets)
    return balance is not None and balance >= amount

# Blockchain
def get_blockchain():
    return load_json("blockchain.json")

def save_blockchain(blockchain):
    save_json("blockchain.json", blockchain)

def add_to_blockchain(transaction):
    blockchain = get_blockchain()
    previous_hash = blockchain[-1]["hash"] if blockchain else None
    timestamp = time.time()
    block_string = f"{previous_hash}{transaction['from']}{transaction['to']}{transaction['amount']}{timestamp}"
    block_hash = hashlib.sha256(block_string.encode()).hexdigest()

    new_block = {
        "timestamp": timestamp,
        "previous_hash": previous_hash,
        "transactions": [transaction],
        "hash": block_hash
    }

    blockchain.append(new_block)
    save_blockchain(blockchain)

# Flask-routes
@app.route('/wallet', methods=['GET'])
def wallet():
    public_key = request.args.get('public_key')
    balance = None
    if public_key:
        wallets = get_wallets()
        balance = get_balance(public_key, wallets)
    return render_template("wallet.html", balance=balance, public_key=public_key)

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        from_public_key = request.form.get('from')
        private_key = request.form.get('private')  # Ej använd
        to_public_key = request.form.get('to')

        try:
            amount = float(request.form.get('amount'))
        except (TypeError, ValueError):
            return render_template('send.html', error="Ogiltigt belopp.")

        wallets = get_wallets()

        if get_balance(from_public_key, wallets) is None:
            return render_template('send.html', error="Från public key hittades inte.")
        if get_balance(to_public_key, wallets) is None:
            return render_template('send.html', error="Till public key hittades inte.")
        if not is_valid_transaction(from_public_key, amount, wallets):
            return render_template('send.html', error="Otillräckligt saldo.")

        transaction = create_transaction(from_public_key, to_public_key, amount)
        add_to_mempool(transaction)

        update_balance(from_public_key, get_balance(from_public_key, wallets) - amount, wallets)
        update_balance(to_public_key, get_balance(to_public_key, wallets) + amount, wallets)
        save_wallets(wallets)

        add_to_blockchain(transaction)

        return render_template('send.html', success=True)

    return render_template('send.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
