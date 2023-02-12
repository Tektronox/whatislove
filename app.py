import json
from flask import Flask, render_template, request, jsonify
from random import shuffle

QUESTION_FILE = 'questions.json'
with open(QUESTION_FILE) as f:
    questions = json.load(f)
    questions = questions['questions']

q_a_pairs = []
answers_release = False
question_idx = 0

app = Flask(__name__)



@app.route('/')
def index():
    global question_idx
    question = questions[question_idx]
    question_idx += 1
    if question_idx >= len(questions):
        question_idx = 0
    return render_template('index.html', question=question)

@app.route('/release-answers', methods=['POST'])
def release_answers():
    global answers_release
    global q_a_pairs
    global question_idx
    answers_release = True
    question_idx = 0
    print("shuffling q_a_pairs")
    shuffle(q_a_pairs)
    return 'success'

@app.route('/reset', methods=['POST'])
def reset():
    global answers_release
    global q_a_pairs
    global question_idx
    answers_release = False
    q_a_pairs = []
    question_idx = 0
    return 'success'

@app.route('/answer', methods=['POST', 'GET'])
def answer():
    if request.method == "POST":
        answer = request.form['answer']
        question = request.form['question']
        q_a = (question, answer)
        print(q_a)
        q_a_pairs.append(q_a)
        print(f"Total answers: {len(q_a_pairs)}")
        return render_template('answer_wait.html')
    
@app.route('/results')
def results():
    global question_idx
    global q_a_pairs
    
    question, answer = q_a_pairs[question_idx]
    question_idx += 1
    if question_idx >= len(q_a_pairs):
        question_idx = 0
    return render_template('answers_released.html', question=question, answer=answer)

@app.route('/answer-wait')
def answer_wait():
    return jsonify({'released': answers_release})

    

app.run(debug=True)