from random import randint
from flask import Flask, redirect, request, render_template
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


@app.route('/playgame', methods=['GET'])
def load_screen():
    global difficulty, secret_number
    difficulty = int(request.args.get('difficulty'))
    generate_number()
    return render_template('guess.html', difficulty=difficulty)


@app.route('/gg_answer', methods=['GET'])
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
    return render_template('answer.html', color=color, text=text, difficulty=difficulty)

def save_score():
    global difficulty
    Score.connect_db()
    Score.add_score(difficulty)
    Score.disconnect_db()

app.run(host="0.0.0.0", port=80, debug=False)
