import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import json
import hashlib
from datetime import datetime

def get_latest_match():
    url = "https://www.gokgs.com/gameArchives.jsp?user=aspectu"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'grid'})

        if table:
            rows = table.find_all('tr')[1:]
            for row in rows:
                columns = row.find_all('td')
                if len(columns) > 6:
                    result = columns[6].text.strip()
                    if result.lower() != 'unfinished':
                        viewable = columns[0].text.strip()
                        white_player = columns[1].text.strip()
                        black_player = columns[2].text.strip()
                        setup = columns[3].text.strip()
                        start_time = columns[4].text.strip()
                        game_type = columns[5].text.strip()

                        return {
                            'viewable': viewable,
                            'white': white_player,
                            'black': black_player,
                            'setup': setup,
                            'start_time': start_time,
                            'type': game_type,
                            'result': result
                        }
    return None

def read_saved_match():
    if not os.path.exists('matches.csv'):
        return None

    with open('matches.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
        if len(rows) < 2:
            return None
        return rows[1]

def save_match(match):
    with open('matches.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Viewable', 'White', 'Black', 'Setup', 'Start Time', 'Type', 'Result'])
        writer.writerow([
            match['viewable'],
            match['white'],
            match['black'],
            match['setup'],
            match['start_time'],
            match['type'],
            match['result']
        ])

def match_to_list(match):
    return [
        match['viewable'],
        match['white'],
        match['black'],
        match['setup'],
        match['start_time'],
        match['type'],
        match['result']
    ]

def load_blockchain():
    if not os.path.exists('blockchain.json'):
        return []
    with open('blockchain.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def save_blockchain(blockchain):
    with open('blockchain.json', 'w', encoding='utf-8') as file:
        json.dump(blockchain, file, indent=4)

def calculate_hash(data):
    block_string = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def add_block(match):
    blockchain = load_blockchain()
    previous_hash = blockchain[-1]['hash'] if blockchain else None

    block_data = {
        'index': len(blockchain) + 1,
        'timestamp': time.time(),
        'previous_hash': previous_hash,
        'match_data': {
            'Viewable': match['viewable'],
            'White': match['white'],
            'Black': match['black'],
            'Setup': match['setup'],
            'Start Time': match['start_time'],
            'Type': match['type'],
            'Result': match['result']
        }
    }

    block_hash = calculate_hash(block_data)
    block_data['hash'] = block_hash

    blockchain.append(block_data)
    save_blockchain(blockchain)
    print("Block tillagd i blockchain.json.")

# 👉 Scraping-loopen som funktion att starta i en bakgrundstråd
def run_scraper():
    while True:
        latest_match = get_latest_match()
        if latest_match:
            saved_match = read_saved_match()
            if saved_match != match_to_list(latest_match):
                save_match(latest_match)
                add_block(latest_match)
                print("NY MATCH HAR SPELATS OCH LAGTS TILL I MATCHES.CSV & BLOCKCHAIN.JSON:")
                print(f"{latest_match['start_time']} - {latest_match['white']} vs {latest_match['black']}, Result: {latest_match['result']}")
            else:
                print("Ingen ny match än...")
        else:
            print("Kunde inte hämta matchdata.")
        time.sleep(30)
