import os
from flask import Flask, render_template, request, jsonify
from gigachatAPI.utils.help_methods import *
from intermediate_state_back.compose_response import get_result_from_file, get_result_from_text
from gigachatAPI.main import generate_questions
from gigachatAPI.answering_questions.answer_questions import get_answer

Shad = Flask(__name__)


@Shad.route('/')
def index():
    return render_template('index.html')


@Shad.route('/request')
def test_page():
    return render_template('request.html')


@Shad.route('/process_file', methods=['POST'])
def process_file():
    uploaded_file = request.files['file']
    que_num_req = request.form['text-number-of-questions']
    que_num = int(que_num_req) if que_num_req and que_num_req.isdigit() else 5
    uploaded_text = request.form['text-generation']

    if uploaded_file.filename:
        result = get_result_from_file(generate_questions, uploaded_file, que_num)
    elif uploaded_text:
        result = get_result_from_text(generate_questions, uploaded_text, que_num)
    else:
        return jsonify({'result': 'Ошибка: файл не выбран'})

    return jsonify({'result': result})


@Shad.route('/process_answer_questions', methods=['POST'])
def procces_answer_questions():
    uploaded_file = request.files['file']
    uploaded_text = request.form['text_for_search_answers']
    asked_questions = [request.form['asked_questions_text']]

    if uploaded_file.filename:
        result = get_result_from_file(get_answer, uploaded_file, asked_questions)
    elif uploaded_text:
        result = get_result_from_file(generate_questions, uploaded_file, asked_questions)
    else:
        return jsonify({'result': 'Ошибка: файл не выбран'})

    return jsonify({'result': result})


if __name__ == '__main__':
    Shad.run(debug=True)
