from flask import Flask, redirect, request

app = Flask(__name__)

"""from Live import welcome,load_game

print(welcome("Evyatar"))
load_game()"""

@app.route('/welcome', methods=['GET'])
def welcome():
    return "<html><head><title>" + "\n" \
           "World of games</title>" + "\n" \
           "<script>" + "\n" \
            "	function playgame(){" + "\n" \
            "		var url = 'http://'+ window.location.hostname + ':' + window.location.port +'/gamepicker';" + "\n" \
            "		window.open(url, '_self')" + "\n" \
            "	}" + "\n" \
            "</script></head>" + "\n" \
           "<body>" + "\n" \
           "<h1>Welcome to the world of games!</h1>" + "\n" \
           "<br>" + "\n" \
           "<button type='button' onclick='playgame()'>Click here to play</button>" \
           "</body></html>"

@app.route('/gamepicker', methods=['GET'])
def game_picker():
    return  "" + "\n" \
            "<html><head><title> " + "\n" \
            "World of games</title>" + "\n" \
            "<script>" + "\n" \
            "	function playgame(){" + "\n" \
            "		var e = document.getElementById('games');" + "\n" \
            "		var gameName = e.options[e.selectedIndex].value;" + "\n" \
            "		var url = null" + "\n" \
            "		switch(gameName)" + "\n" \
            "		{" + "\n" \
            "			case 'memorygame':" + "\n" \
            "				url = 'http://'+ window.location.hostname + '/memorygame';" + "\n" \
            "				break;" + "\n" \
            "			case 'guessgame':" + "\n" \
            "				url = 'http://'+ window.location.hostname + '/guessgame';" + "\n" \
            "				break;" + "\n" \
            "			case 'currecyrollete':" + "\n" \
            "				url = 'http://'+ window.location.hostname + '/currecyrollete';" + "\n" \
            "				break;" + "\n" \
            "			case 'score':" + "\n" \
            "				url = 'http://'+ window.location.hostname + '/getscore';" + "\n" \
            "				break;" + "\n" \
            "		}" + "\n" \
            "		var f = document.getElementById('difficulty');" + "\n" \
            "		var difficulty = f.options[f.selectedIndex].value;" + "\n" \
            "		url += '?difficulty=' + difficulty;" + "\n" \
            "		window.open(url)" + "\n" \
            "	}" + "\n" \
            "</script>" + "\n" \
            "</head><body>" + "\n" \
            "<h1>Choose a game to play</h1>" + "\n" \
            "<br>" + "\n" \
            "<label for='games'>Choose a game to play</label>" + "\n" \
            "<select id='games'>" + "\n" \
            "  <option value='memorygame' selected>Memory Game</option>" + "\n" \
            "  <option value='guessgame'>Guess Game</option>" + "\n" \
            "  <option value='currecyrollete'>Currency Roulette</option>" + "\n" \
            "  <option value='score'>See your Score</option>" + "\n" \
            "</select>" + "\n" \
            "<br>" + "\n" \
            "<label for='difficulty'>Choose difficulty</label>" + "\n" \
            "<select id='difficulty'>" + "\n" \
            "  <option value='1' selected>1</option>" + "\n" \
            "  <option value='2'>2</option>" + "\n" \
            "  <option value='3'>3</option>" + "\n" \
            "  <option value='4'>4</option>" + "\n" \
            "  <option value='5'>5</option>" + "\n" \
            "</select>" + "\n" \
            "<br><br>" + "\n" \
            "<button  type='button' onclick='playgame()'>Start Playing</button>" + "\n" \
            "</body></html>"

app.run(host="0.0.0.0", port=80, debug=False)