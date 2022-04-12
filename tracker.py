import requests
import time

# CONSTANTS  ----- MUST REPLACE BOT_TOKEN & CHAT_ID
API_KEY = "09a9c492-87d0-4d44-88bc-81ee612de88d"
BOT_TOKEN = "5145309949:AAHxw-NNkx0fPhl64JbX_SVa3s6n8BuxM-Y"  
CHAT_ID = "YOUR TELEGRAM CHAT-ID HERE" # (Ex: 509574533)

THRESHOLD = 41000
UPHOLD = 42000
TIME_INTERVAL = 5 * 60


def get_btc_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }
    # Make a request to the coinmarketcap api
    response = requests.get(url, headers=headers)
    response_json = response.json()

    # Extract the bitcoin price from the json data
    btc_price = response_json['data'][0]
    return btc_price['quote']['USD']['price']


# Fn to send_message through telegram
def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"

    # send the msg
    requests.get(url)


# main fn
def main():
    price_list = []

    # infinite loop
    while True:
        price = get_btc_price()
        price_list.append(price)

    # if the price falls below threshold, send an immediate msg
        if price < THRESHOLD:
            send_message(chat_id=CHAT_ID, msg=f'BTC Price Drop Alert: {price}')

    # if the price falls below threshold, send an immediate msg
        if price > UPHOLD:
            send_message(chat_id=CHAT_ID, msg=f'BTC Price Rise Alert: {price}')

        # send the last 6 btc price
        if len(price_list) >= 6:
            send_message(chat_id=CHAT_ID, msg=price_list)
            # empty the price list
            price_list = []

    # fetch the price for every dash minutes
        time.sleep(TIME_INTERVAL)


# fancy way to activate the main() fn
if __name__ == '__main__':
    main()
