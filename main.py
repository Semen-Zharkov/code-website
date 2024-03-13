from flask import Flask, render_template, request, jsonify
from intermediate_state_back.compose_response import get_result_from_file, get_result_from_text, del_if_exist
from gigachatAPI.generate_test import generate_questions
from gigachatAPI.answering_questions.answer_questions import get_answer

Shad = Flask(__name__)


@Shad.route('/')
def index():
    return render_template('index.html')


@Shad.route('/request')
def test_page():
    return render_template('request.html')


@Shad.route('/test')
def request_page():
    return render_template('test.html')


@Shad.route('/process_file', methods=['POST'])
def process_file(ans_aft_que=False):
    del_if_exist()
    uploaded_file = request.files['file']
    que_num_req = request.form['text-number-of-questions']
    que_num = int(que_num_req) if que_num_req and que_num_req.isdigit() else 5
    uploaded_text = request.form['text-generation']

    if uploaded_file.filename:
        result = get_result_from_file(generate_questions, uploaded_file, ans_aft_que, que_num)
    elif uploaded_text:
        result = get_result_from_text(generate_questions, uploaded_text, ans_aft_que, que_num)
    else:
        result = 'Добавьте файл или вставьте текст!'

    return jsonify({'result': result})


@Shad.route('/process_answer_questions', methods=['POST'])
def process_answer_questions(ans_aft_que=False):
    del_if_exist()
    uploaded_file = request.files['file']
    asked_questions = list(filter(None, request.form['asked_questions_text'].split(';')))

    if uploaded_file.filename:
        result = get_result_from_file(get_answer, uploaded_file, ans_aft_que, asked_questions)
    else:
        result = 'Добавьте файл или вставьте текст!'

    return jsonify({'result': result})


if __name__ == '__main__':
    Shad.run(debug=True, host='0.0.0.0')
