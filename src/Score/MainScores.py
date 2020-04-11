import Score
from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/getscore', methods=['GET'])
def score_server():
    html = None
    try:
        Score.connect_db()
        score = Score.read_score_from_db()
        html = f"<html><head><title>Scores Game</title></head><body><h1>The score is <div id=\"score\">{score}</div></h1></body></html>"
    except BaseException as e:
        html = f"<html><head><title>Scores Game</title></head><body><body><h1><div id=\"score\" style=\"color:red\">{e}</div></h1></body></html>"
    Score.disconnect_db()
    return html

app.run(host="0.0.0.0", port=80, debug=False)
