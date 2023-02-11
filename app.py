import json
from flask import Flask, render_template, request
from random import shuffle

QUESTION_FILE = 'questions.json'
with open(QUESTION_FILE) as f:
    questions = json.load(f)
    questions = questions['questions']

q_a_pairs = []
answers_release = False

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/release-answers', methods=['POST'])
def release_answers():
    global answers_release
    global q_a_pairs
    answers_release = True
    print("shuffling q_a_pairs")
    shuffle(q_a_pairs)
    return 'success'

@app.route('/answer', methods=['POST', 'GET'])
def answer():
    if request.method == "POST":
        answer = request.form['answer']
        question = request.form['question']
        q_a_pairs.append((question, answer))
        print(f"Total answers: {len(q_a_pairs)}")
        return render_template('answers.html')

    elif request.method == "GET":
        return render_template('answers.html', q_a_pairs=q_a_pairs)

@app.route('/admin')
def admin():
    return render_template('admin.html')

    

app.run(debug=True)