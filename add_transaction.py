# add_transaction.py
import json
import time

def add_transaction(sender, recipient, amount):
    transaction = {
        "from": sender,
        "to": recipient,
        "amount": amount,
        "timestamp": time.time()
    }

    with open("mempool.json", "r") as f:
        mempool = json.load(f)

    mempool.append(transaction)

    with open("mempool.json", "w") as f:
        json.dump(mempool, f, indent=4)
