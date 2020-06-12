from random import randint
from flask import Flask, redirect, request, render_template
import Score

app = Flask(__name__)

difficulty = -1
MAX_NUMBER = 101
TIME = 0.7
comp_list = []

def generate_sequence():
    global difficulty, MAX_NUMBER, TIME
    list = []
    for i in range(difficulty):
        list.append(randint(1,MAX_NUMBER))
    return list

def is_list_equal(list1, list2):
    if len(list1) != len(list2):
        return False
    are_equal = True
    i = 0
    try:
        while i < len(list1) and are_equal:
            are_equal = int(list1[i]) == int(list2[i])
            i+=1
    except ValueError as e:
        raise ValueError("Must me numeric")
    return are_equal


@app.route('/playgame', methods=['GET'])
def load_screen():
    global difficulty, TIME, comp_list
    difficulty = int(request.args.get('difficulty'))
    comp_list = generate_sequence()
    join_list = ','.join(str(x) for x in comp_list)
    return render_template('memory.html', time=TIME * 1000, join_list=join_list)


@app.route('/mg_answer', methods=['GET'])
def play():
    global difficulty, comp_list
    try:
        user_list = request.args.get('numbers').split(',')
        join_list = ','.join(str(x) for x in comp_list)
        user_won = is_list_equal(user_list, comp_list)
        if user_won:
            text = "Congrats! you won!"
            color = "black"
            save_score()
        else:
            text = f"Sorry, you lost. the sequence was {join_list}"
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
