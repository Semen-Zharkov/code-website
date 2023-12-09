import os
from gigachatAPI.utils.help_methods import *
from gigachatAPI.main import generate_questions
from flask import Flask, render_template, url_for, request, jsonify
from gigachatAPI.config_data.config_data import *
from gigachatAPI.answering_questions.answer_questions import get_answer

Shad = Flask(__name__)


@Shad.route('/')
def index():
    return render_template('index.html')


@Shad.route('/request')
def test_page():
    return render_template('request.html')


@Shad.route('/process_file', methods=['POST'])
def process_file(dita=0):
    uploaded_file = request.files['file']
    que_num = request.form['text-number-of-questions']
    if que_num and que_num.isdigit():
        que_num = int(que_num)
    uploaded_text = request.form['text-generation']
    asked_question = request.form['text-questions']

    if uploaded_file.filename != '':
        file_path = os.path.join('gigachatAPI/data', uploaded_file.filename)
        uploaded_file.save(file_path)

        if uploaded_file.filename.split('.')[-1] == 'zip':
            dita = 1
            unpack_path = 'gigachatAPI/data/extract_zip'
            extract_zip(file_path, unpack_path)
            os.remove(file_path)
            file_path = unpack_path

        if asked_question:
            result = get_answer(file_path, 'gigachatAPI/prompts/qna_system.yaml',
                                'gigachatAPI/prompts/qna_user.yaml', [asked_question], dita=dita)
        else:
            result = generate_questions(file_path, gen_que_sys_prompt_path,
                                        gen_que_usr_prompt_path, que_num, dita=dita)

        del_dir(file_path) if dita == 1 else os.remove(file_path)
        return jsonify({'result': result})
    elif uploaded_text:
        file_path = os.path.join('gigachatAPI/data', 'file_for_gen_que')
        with open(file_path, 'w', encoding='utf-8') as file_for_write:
            file_for_write.write(uploaded_text)
        if asked_question:
            result = get_answer(file_path, 'gigachatAPI/prompts/qna_system.yaml',
                                'gigachatAPI/prompts/qna_user.yaml', [asked_question], dita=0)
        else:
            result = generate_questions(file_path, gen_que_sys_prompt_path,
                                        gen_que_usr_prompt_path, que_num, dita=0)
        os.remove(file_path)
        return jsonify({'result': result})


if __name__ == '__main__':
    Shad.run(debug=True)
