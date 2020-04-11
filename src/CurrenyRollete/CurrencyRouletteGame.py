from random import randint
import requests
import json
import Score
from flask import Flask, redirect, request

app = Flask(__name__)


CURRENCY_URL = "http://www.floatrates.com/daily/usd.json"
MAX_NUMBER = 100
difficulty = -1
ils_usd_rate = -1
usd_amount = -1

def load_currency_rate():
    global ils_usd_rate, CURRENCY_URL
    response = requests.get(CURRENCY_URL)
    ils_usd_rate = float(json.loads(response.content)["ils"]["rate"])

def get_money_interval(ils_amount):
    global difficulty
    return (round(ils_amount - (5 - difficulty)),round(ils_amount + (5 - difficulty)))

def get_guess_from_user():
    global MAX_NUMBER, usd_amount
    usd_amount = randint(1, MAX_NUMBER)
    return float(input('How much {} dollars are in shekels?: '.format(usd_amount)))

@app.route('/currecyrollete', methods=['GET'])
def load_screen():
    global difficulty, usd_amount
    difficulty = int(request.args.get('difficulty'))
    load_currency_rate()
    usd_amount = randint(1, MAX_NUMBER)
    return "<html><head><title>" + "\n" \
           "World of games - Currency Rollete Game</title>" + "\n" \
           "</head>" + "\n" \
           "<script>" + "\n" \
           "	function playgame(){" + "\n" \
           "		var e = document.getElementById('shekels');" + "\n" \
           "		var result = e.value;" + "\n" \
           "		var url = 'http://' + window.location.hostname + ':' + window.location.port + '/answer?shekels=' + result" + "\n" \
           "		console.log(url);" + "\n" \
           "		window.open(url, '_self')" + "\n" \
           "	}" + "\n" \
           "</script>" + "\n" \
           "<body>" + "\n" \
           "<h1>Curreny Rollete Game</h1>" + "\n" \
           "<br>" + "\n" \
           f"How much is <div id='dollars' style='color:red'>{usd_amount}</div> dollars worth in shekels?<br>" + "\n" \
           "<input type='text' id='shekels'>" + "\n" \
           "<br><br>" + "\n" \
           "<button id='btn_play' type='button' onclick='playgame()'>Play</button>" + "\n" \
           "</body>" + "\n" \
           "</html>"

@app.route('/answer', methods=['GET'])
def play():
    global difficulty,usd_amount, ils_usd_rate
    try:
        user_answer = float(request.args.get('shekels'))
        real_value = int(usd_amount * ils_usd_rate)
        money_interval = get_money_interval(real_value)
        user_won = user_answer >= money_interval[0] and user_answer <= money_interval[1]
        if user_won:
            text = "Congrats! you won!"
            color = "black"
            save_score()
        else:
            text = f"Sorry, you lost. the value is {real_value}"
            color = "red"
    except ValueError as e:
        text = e
        color = "red"
    return f"<html><head>" + "\n" \
           f"<title>Memory Game</title>" + "\n" \
           "<script>" + "\n" \
           "function playagain(){" + "\n" \
           f"	var url = 'http://' + window.location.hostname + ':' + window.location.port + '/currecyrollete?difficulty=' + {difficulty}" + "\n" \
           "	console.log(url);" + "\n" \
           "	window.open(url, '_self')" + "\n" \
           "}" + "\n" \
           f"</script>" + "\n" \
           f"</head><body>" + "\n" \
           f"<h1><div id='answer' style=\"color:{color}\">" + "\n" \
           f"{text}</div></h1>" + "\n" \
           f"<br><br>" + "\n" \
           f"<button  type='button' onclick='playagain()'>Play Again</button>" + "\n" \
           f"</body>" + "\n" \
           f"</html>"

def save_score():
    global difficulty
    Score.connect_db()
    Score.add_score(difficulty)
    Score.disconnect_db()

app.run(host="0.0.0.0", port=80, debug=False)
