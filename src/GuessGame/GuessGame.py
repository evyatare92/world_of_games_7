from random import randint
from flask import Flask, redirect, request
import Score

app = Flask(__name__)

difficulty = -1
secret_number = -1

def validate_user_num(user_num,minimum = 1, maximum = None):
    num = -1

    if maximum != None and maximum < minimum:
        raise ValueError("wrong borders")
    try:
        num = int(user_num)
        if num < minimum:
            raise ValueError("the number must be greater than or equal to {}".format(minimum))
        elif maximum != None and num > maximum:
            raise ValueError("the number must be less than {}".format(maximum))
    except ValueError as e:
        raise ValueError("must be numeric")

    return num

def generate_number():
    global difficulty, secret_number
    secret_number = randint(1, difficulty)
    return secret_number

def compare_results(user_num):
    global secret_number
    user_num = validate_user_num(user_num)
    return user_num == secret_number

@app.route('/guessgame', methods=['GET'])
def load_screen():
    global difficulty, secret_number
    difficulty = int(request.args.get('difficulty'))
    generate_number()
    return "<html><head><title>" + "\n" \
           "World of games - Guess Game</title>" + "\n" \
           "</head>" + "\n" \
           "<script>" + "\n" \
           "	function playgame(){" + "\n" \
           "		var e = document.getElementById('choise');" + "\n" \
           "		var result = e.value;" + "\n" \
           "		var url = 'http://' + window.location.hostname + ':' + window.location.port + '/answer?user_num=' + result" + "\n" \
           "		console.log(url);" + "\n" \
           "		window.open(url, '_self')" + "\n" \
           "	}" + "\n" \
           "</script>" + "\n" \
           "<body>" + "\n" \
           "<h1>Guess Game</h1>" + "\n" \
           "<br>" + "\n" \
           f"<label for='choise'>Please enter a number between 1 and {difficulty}:</label>" + "\n" \
           "<input type='text' id='choise'>" + "\n" \
           "<br><br>" + "\n" \
           "<button id='btn_play' type='button' onclick='playgame()'>Play</button>" + "\n" \
           "</body>" + "\n" \
           "</html>"

@app.route('/answer', methods=['GET'])
def play():
    global difficulty, secret_number
    user_num = request.args.get('user_num')
    user_won = compare_results(user_num)
    try:
        if user_won:
            text = "Congrats! you won!"
            color = "black"
            save_score()
        else:
            text = f"Sorry, you lost. the secret number was {secret_number}"
            color = "red"
    except BaseException as e:
        text = e
        color = "red"
    return  f"<html><head>" + "\n" \
            f"<title>Guess Game</title>" + "\n" \
            f"<script>" + "\n" \
            "function playagain(){" + "\n" \
            f"		var url = 'http://' + window.location.hostname + ':' + window.location.port + '/guessgame?difficulty=' + {difficulty}" + "\n" \
            "		console.log(url);" + "\n" \
            "		window.open(url, '_self')" + "\n" \
            "	}" + "\n" \
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
