import hashlib
import json
import time
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Funktion för att läsa plånböcker från wallets.json
def get_wallets():
    try:
        with open("wallets.json", "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading wallets.json: {e}")
        return []

# Funktion för att skriva tillbaka plånböcker till wallets.json
def save_wallets(wallets):
    try:
        with open("wallets.json", "w") as file:
            json.dump(wallets, file, indent=4)
    except Exception as e:
        print(f"Error saving wallets.json: {e}")

# Funktion för att läsa mempool från mempool.json
def get_mempool():
    try:
        with open("mempool.json", "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading mempool.json: {e}")
        return []

# Funktion för att skriva tillbaka mempool till mempool.json
def save_mempool(mempool):
    try:
        with open("mempool.json", "w") as file:
            json.dump(mempool, file, indent=4)
    except Exception as e:
        print(f"Error saving mempool.json: {e}")

# Funktion för att läsa blockchain från blockchain.json
def get_blockchain():
    try:
        with open("blockchain.json", "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading blockchain.json: {e}")
        return []

# Funktion för att skriva tillbaka blockchain till blockchain.json
def save_blockchain(blockchain):
    try:
        with open("blockchain.json", "w") as file:
            json.dump(blockchain, file, indent=4)
    except Exception as e:
        print(f"Error saving blockchain.json: {e}")

# Funktion för att hämta saldo för en specifik public_key
def get_balance(public_key):
    wallets = get_wallets()
    for wallet in wallets:
        if wallet['public_key'] == public_key:
            return wallet['balance']
    return None

# Funktion för att uppdatera saldo för en specifik public_key
def update_balance(public_key, new_balance):
    wallets = get_wallets()
    for wallet in wallets:
        if wallet['public_key'] == public_key:
            wallet['balance'] = new_balance
            save_wallets(wallets)  # Spara uppdaterade plånböcker till wallets.json
            return True
    return False

# Funktion för att skapa transaktion
def create_transaction(from_public_key, to_public_key, amount):
    transaction = {
        "from": from_public_key,
        "to": to_public_key,
        "amount": amount,
        "timestamp": time.time(),
        "hash": hashlib.sha256(f"{from_public_key}{to_public_key}{amount}{time.time()}".encode()).hexdigest()
    }
    return transaction

# Funktion för att lägga till en transaktion i mempoolen
def add_to_mempool(transaction):
    mempool = get_mempool()
    mempool.append(transaction)
    save_mempool(mempool)

# Funktion för att flytta transaktioner från mempool till blockchain
def add_to_blockchain(transaction):
    blockchain = get_blockchain()
    if blockchain:
        previous_hash = blockchain[-1]["hash"]
    else:
        previous_hash = None
    new_block = {
        "timestamp": time.time(),
        "previous_hash": previous_hash,
        "transactions": [transaction],
        "hash": hashlib.sha256(f"{previous_hash}{transaction['from']}{transaction['to']}{transaction['amount']}{time.time()}".encode()).hexdigest()
    }
    blockchain.append(new_block)
    save_blockchain(blockchain)

@app.route('/wallet', methods=['GET'])
def wallet():
    public_key = request.args.get('public_key')
    balance = None
    if public_key:
        balance = get_balance(public_key)
    return render_template("wallet.html", balance=balance, public_key=public_key)

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        from_public_key = request.form.get('from')
        private_key = request.form.get('private')  # Not used in this case, just for form
        to_public_key = request.form.get('to')
        amount = float(request.form.get('amount'))

        from_balance = get_balance(from_public_key)
        to_balance = get_balance(to_public_key)

        if from_balance is None:
            return render_template('send.html', error="Från public key hittades inte.")
        if to_balance is None:
            return render_template('send.html', error="Till public key hittades inte.")
        if from_balance < amount:
            return render_template('send.html', error="Otillräckligt saldo för att skicka tokens.")

        # Skapa transaktion
        transaction = create_transaction(from_public_key, to_public_key, amount)

        # Lägg till transaktionen i mempool
        add_to_mempool(transaction)

        # Uppdatera saldon
        new_from_balance = from_balance - amount
        new_to_balance = to_balance + amount
        update_balance(from_public_key, new_from_balance)
        update_balance(to_public_key, new_to_balance)

        # Lägg till transaktionen i blockchain när den bekräftas
        add_to_blockchain(transaction)

        return render_template('send.html', success=True)

    return render_template('send.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
