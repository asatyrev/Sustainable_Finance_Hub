from flask import Flask, request, render_template_string
import google.generativeai as genai
import requests

app = Flask(__name__)

api_key = "TOKEN GOES HERE"

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
    response = chat_session.send_message("can you give me the most eco friendly companies in this format: ['NVDA', 'AAPL', 'AMZN', 'META'] (replace them with the company tags) please dont say anything else apart from this")
    symbols = eval(response.text)
    response2 = chat_session.send_message(f"{response} you chose these companies as the most eco friendly can you give me a short paragraph of about 100 words on why you think so")
    
    prices = nstock(date)

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Stock Prices</title>
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/styles.css') }}">
        </head>
        <body>
        <h1 id="Title">Response from Gemini and FMP</h1>
        <div class="content-container">
        
        <h2>Stock Prices for {{ selected_date }}</h2>
        <ul>
            {% for symbol, price in stock_prices %}
                <li>{{ symbol }}: {{ price }}</li>
            {% endfor %}
        </ul>

        <p id="resp">{{ response_text }}</p>

        <form method="post" class="form-container">
            <div class="form-controls">
            <label for="date">Select Date:</label>
            <input type="date" id="date" name="date" value="{{ selected_date }}">
            <input type="submit" value="Submit">
        </div>
        <button type="button" onclick="window.location.href='{{ url_for('new_page') }}'">Go To Carbon Calculator</button>
    </form>
        </div>
        </body>
        </html>
    ''', response_text=response2.text, stock_prices=zip(symbols, prices), selected_date=date)


@app.route('/new-page')
def new_page():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}">
        <title>Carbon Footprint Tracker</title>
    </head>
    <body>
        <h1 id="Title">Carbon Footprint Calculator</h1>
        <div id="explanation">
            <img id="photo" src="{{ url_for('static', filename='terrahacks.jpg') }}" alt="Photo of an image">
            <div class="text-content">
                <p>
                    Understanding your carbon footprint is crucial in making informed decisions about how to reduce your impact on the environment. A carbon footprint measures the total amount of greenhouse gases emitted into the atmosphere as a result of various activities, including electricity usage, transportation, and more. By tracking and managing your carbon footprint, you contribute to the fight against climate change and work towards a more sustainable future. Below is a calculator to track your carbon footprint and based on your data, there will be some tips on how to lower your footprint!
                </p>
            </div>
        </div>
        <div class="form-container">
            <div class="input-container" id="electricity">
                <label>Electricity bill per month</label>
                <input type="number" placeholder="Enter amount in dollars">
            </div>
            <div class="input-container" id="gas">
                <label>Gas bill per month</label>
                <input type="number" placeholder="Enter amount in dollars">
            </div>
            <div class="input-container" id="mileage">
                <label>Total mileage on vehicles</label>
                <input type="number" placeholder="Enter total miles">
            </div>
            <div class="input-container" id="flights">
                <label>Total amount of flights in the past year</label>
                <input type="number" placeholder="Enter number of flights">
            </div>
            <div class="input-container" id="water">
                <label>Monthly water usage (in gallons)</label>
                <input type="number" placeholder="Enter amount in gallons">
            </div>
            <div class="input-container" id="food">
                <label>Monthly food consumption</label>
                <input type="number" placeholder="Enter amount in dollars">
            </div>
            <div id="calculate">
                <button type="submit">Calculate</button>
            </div>
            <div id="results">
                <p id="result-text">Your results will appear here.</p>
            </div>        
        </div>
        <button onclick="location.href='{{ url_for('index') }}'">Go to Eco Stocks</button>
        <script src="{{ url_for('static', filename='js/carbon.js') }}"></script>
    </body>
    </html>
    ''')


def nstock(date):
    api_key = 'TOKEN GOES HERE'
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
