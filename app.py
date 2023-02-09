import flask
import json

QUESTION_FILE = 'questions.json'
with open(QUESTION_FILE) as f:
    questions = json.load(f)
    questions = questions['questions']


app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html', questions=questions)


@app.route('/answer', methods=['POST'])
def answer():
    answer = flask.request.form['answer']
    question = flask.request.form['question']
    correct = questions[question] == answer
    return flask.render_template('answer.html', correct=correct)

app.run(debug=True)