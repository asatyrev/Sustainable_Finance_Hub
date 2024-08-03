from flask import Flask, request, render_template_string
import google.generativeai as genai
import requests

app = Flask(__name__)

api_key = "AIzaSyAkhI7RtlOZwfJ12kWH0us8fZVX6qcMMzk"

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

symbols = []

from datetime import datetime, timedelta

def get_date():
    today = datetime.now()

    if today.weekday() in [5, 6]:
        days_since_friday = (today.weekday() - 4) % 7
        last_friday = today - timedelta(days=days_since_friday)
        return last_friday.strftime('%Y-%m-%d')
    else:
        return today.strftime('%Y-%m-%d')


@app.route('/', methods=['GET', 'POST'])
def index():
    global symbols
    date = get_date()

    if request.method == 'POST':
        date = request.form.get('date')
        
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message("can you give me the most eco friendly companies in this format: ['NVDA', 'AAPL', 'AMZN', 'META'] (replace them with the company tags) please dont say anything else apart form this")
    symbols = eval(response.text)
    
    prices = nstock(date)

    return render_template_string('''
        <html>
        <body>
            <h1>AI</h1>
            <pre>{{ response_text }}</pre>
            <h2>Stock Prices for {{ selected_date }}</h2>
            <ul>
                {% for symbol, price in stock_prices %}
                    <li>{{ symbol }}: {{ price }}</li>
                {% endfor %}
            </ul>
            <form method="post">
                <label for="date">Select Date:</label>
                <input type="date" id="date" name="date" value="{{ selected_date }}">
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
        ''', response_text=response.text, stock_prices=zip(symbols, prices), selected_date=date)

def nstock(date):
    api_key = 'u6iWVDmkSjt5Fhr3zoAko3jCatFP0QJJ'
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

if __name__ == '__main__':
    app.run(debug=True)
