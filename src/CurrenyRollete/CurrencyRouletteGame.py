from random import randint
import requests
import json
import Score
from flask import Flask, redirect, request, render_template

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


@app.route('/playgame', methods=['GET'])
def load_screen():
    global difficulty, usd_amount
    difficulty = int(request.args.get('difficulty'))
    load_currency_rate()
    usd_amount = randint(1, MAX_NUMBER)
    return render_template('currecy.html', usd_amount=usd_amount)


@app.route('/cr_answer', methods=['GET'])
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
    return render_template('answer.html', color=color, text=text, difficulty=difficulty)

def save_score():
    global difficulty
    Score.connect_db()
    Score.add_score(difficulty)
    Score.disconnect_db()

app.run(host="0.0.0.0", port=80, debug=False)
