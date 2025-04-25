mempool = []

def add_to_mempool(transaction):
    # Lägg till en ny transaktion i mempoolen
    mempool.append(transaction)

def get_mempool():
    # Hämta alla transaktioner från mempoolen
    return mempool
