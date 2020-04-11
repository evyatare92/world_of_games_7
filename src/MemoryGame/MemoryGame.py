from random import randint
from time import sleep
from flask import Flask, redirect, request
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

@app.route('/memorygame', methods=['GET'])
def load_screen():
    global difficulty, TIME, comp_list
    difficulty = int(request.args.get('difficulty'))
    comp_list = generate_sequence()
    join_list = ','.join(str(x) for x in comp_list)
    return "<html><head><title>" + "\n" \
           "World of games - Memory Game</title>" + "\n" \
           "</head>" + "\n" \
           "<script>" + "\n" \
           "	function loadgame(){" + "\n" \
           "		var e = document.getElementById('secret');" + "\n" \
           f"		e.innerText = '{join_list}';" + "\n" \
           "		setTimeout(() => { e.innerText = ''; }," \
           f"{TIME * 1000});" + "\n" \
           "	}" + "\n" \
           "	function playgame(){" + "\n" \
           "		var e = document.getElementById('numbers');" + "\n" \
           "		var result = e.value;" + "\n" \
           "		var url = 'http://' + window.location.hostname + ':' + window.location.port + '/answer?numbers=' + result" + "\n" \
           "		console.log(url);" + "\n" \
           "		window.open(url, '_self')" + "\n" \
           "	}" + "\n" \
           "</script>" + "\n" \
           "<body onload='loadgame()'>" + "\n" \
           "<h1>Memory Game</h1>" + "\n" \
           "<br>" + "\n" \
           "<h2>Remember this numbers: </h2>" \
           "<div id='secret' style='color:red'></div><br>" \
           "<label for='numbers'>Please enter the numbers you saw, seperated by commas:</label>" + "\n" \
           "<input type='text' id='numbers'>" + "\n" \
           "<br><br>" + "\n" \
           "<button id='btn_play' type='button' onclick='playgame()'>Play</button>" + "\n" \
           "</body>" + "\n" \
           "</html>"

@app.route('/answer', methods=['GET'])
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
    return f"<html><head>" + "\n" \
        f"<title>Memory Game</title>" + "\n" \
               f"<script>" + "\n" \
                "function playagain(){" + "\n" \
               f"	var url = 'http://' + window.location.hostname + ':' + window.location.port + '/memorygame?difficulty=' + {difficulty}" + "\n" \
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
