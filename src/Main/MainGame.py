from flask import Flask, redirect, request, render_template

app = Flask(__name__)

"""from Live import welcome,load_game

print(welcome("Evyatar"))
load_game()"""

@app.route('/', methods=['GET'])
def welcome():
    return render_template('welcome.html')

@app.route('/gamepicker', methods=['GET'])
def game_picker():
    return render_template('gamepicker.html')

app.run(host="0.0.0.0", port=80, debug=False)