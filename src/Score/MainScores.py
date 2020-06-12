import Score
from flask import Flask, redirect, request, render_template

app = Flask(__name__)

@app.route('/getscore', methods=['GET'])
def score_server():
    try:
        Score.connect_db()
        text = Score.read_score_from_db()
        color = "black"
    except BaseException as e:
        text = e
        color = "red"
    Score.disconnect_db()
    return render_template('score.html', color=color, text=text)

app.run(host="0.0.0.0", port=80, debug=False)
