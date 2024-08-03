from pyscript import document
import requests

def nstock(date):
    api_key = 'u6iWVDmkSjt5Fhr3zoAko3jCatFP0QJJ' # this is my token
    symbols = ['CTVA', 'PHOR.ME', '5285.KL', 'AGCO', '2445.KL'] # the symbol for nvidia
    prices = []

    for symbol in symbols:
        url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={api_key}&serietype=line'
        response = requests.get(url)
        data = response.json()

        found = False


        for item in data.get('historical', []):
            if item['date'] == date:
                prices.append(item['close'])
                found = True
                break
        
        if not found:
            prices.append(None)

    return prices

def getdate(event):
    input_text = document.querySelector("#date")
    date = input_text.value
    output_div = document.querySelector("#output")
    output_div.innerText = nstock(date)
