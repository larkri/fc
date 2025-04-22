import requests
from bs4 import BeautifulSoup
import time
import blockchain  # Importera blockchain-modulen

# URL till spelhistoriken
url = "https://www.gokgs.com/gameArchives.jsp?user=aspectu"

# Håll reda på senaste vinnande spelet
last_game = None


def fetch_and_check_game():
    global last_game

    # Hämta HTML från sidan
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Hitta alla rader i tabellen med resultat (skapar en lista av 'td' taggar)
    rows = soup.find_all('tr')

    for row in rows:
        columns = row.find_all('td')

        if len(columns) > 4:  # säkerställ att raden har tillräckligt med data
            # Extrahera relevant information
            white_player = columns[1].get_text(strip=True)
            black_player = columns[2].get_text(strip=True)
            result = columns[4].get_text(strip=True)

            # Om aspectu spelar och har vunnit (W+ för vit eller B+ för svart)
            if (white_player == "aspectu" and result.startswith("W+")) or (black_player == "aspectu" and result.startswith("B+")):
                # Om ingen tidigare vinst har registrerats eller detta är ett nytt spel
                if last_game is None or last_game != columns[0].get_text(strip=True):
                    print(f"New win detected for aspectu: {columns[0].get_text(strip=True)} - {result}")
                    last_game = columns[0].get_text(strip=True)

                    # Skapa nytt block när aspectu vinner
                    if white_player == "aspectu":
                        blockchain.create_new_block_for_victory(white_player, black_player, result)  # vit vinner
                    else:
                        blockchain.create_new_block_for_victory(black_player, white_player, result)  # svart vinner


# Kör detta varje minut för att hålla koll på nya vinster
while True:
    fetch_and_check_game()
    time.sleep(60)  # Vänta 60 sekunder innan nästa koll
