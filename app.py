from flask import Flask, render_template
from database import CFBDatabase
from config import Config
import random

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Initialize database connection
db = CFBDatabase()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mascot')
def mascot():
    teams = db.get_data_for_four_teams()
    team = teams[0]['school']
    mascot = teams[0]['mascot']
    all_mascots = [mascot, teams[1]['mascot'], teams[2]['mascot'], teams[3]['mascot']]
    random.shuffle(all_mascots)
    return render_template('mascot_quiz.html', team=team, mascot=mascot, all_mascots=all_mascots)

@app.route('/correct')
def correct():
    return render_template('correct.html')

@app.route('/incorrect')
def incorrect():
    return render_template('incorrect.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
