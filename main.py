from pokemontcgsdk import RestClient
from pokemontcgsdk import Card
from pokemontcgsdk import Set


RestClient.configure('82d11068-b3e7-4d17-9753-5f7e424f8b84')
card = Card.find('xy1-1')
# print(card.name)  # "Bulbasaur"
# # print(card)
# print(card.images.large)

# print(Card.where(page=5, pageSize=250))

from flask import Flask, render_template
import requests

app = Flask(__name__)
def parse():
    card_ids = []
    for card in Card.where(page=1, pageSize=10):
        card_ids.append(card.id)
    return card_ids


def display_cards():
    card_ids = parse()
    cards = []

    for card_id in card_ids:
        # Make a request to get the card details using the card_id
        response = requests.get(f'https://api.pokemontcg.io/v2/cards/{card_id}', headers={'X-Api-Key': '123abc'})
        
        if response.status_code == 200:
            card = response.json()['data']
            name = card['name']
            image_url = card['images']['large']
            # Check if 'tcgplayer' and 'prices' keys exist
            prices = None
            if 'tcgplayer' in card and 'prices' in card['tcgplayer']:
                prices_data = card['tcgplayer']['prices']
                
                # Check for the 'market' price in different categories
                if 'holofoil' in prices_data:
                    prices = prices_data['holofoil'].get('market')
                elif 'normal' in prices_data:
                    prices = prices_data['normal'].get('market')
                elif 'reverseHolofoil' in prices_data:
                    prices = prices_data['reverseHolofoil'].get('market')
            pokemon_set = card['set']['name']
            pokemon_series = card['set']['series']
            
            cards.append({'name': name, 'image_url': image_url, 'prices': prices, 'pokemon_set': pokemon_set, 'pokemon_series': pokemon_series})
    
    return cards

@app.route('/')
def home():
    cards = display_cards()
    return render_template('index.html', cards=cards)

# @app.route('/')
# def home():
#     # Use the Pokémon TCG API to get card details
#     response = requests.get('https://api.pokemontcg.io/v2/cards/xy1-1', headers={'X-Api-Key': '123abc'})
    
#     if response.status_code == 200:
#         card = response.json()['data']
#         name = card['name']  # Make sure to use dictionary-style access
#         image_url = card['images']['large']
#     else:
#         name = "Card not found"
#         image_url = ""

#     # Pass the data to the HTML template
#     return render_template('index.html', name=name, image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)

