import os
import shutil
from typing import Callable
from gigachatAPI.utils.help_methods import *
from gigachatAPI.answering_questions.answer_questions import get_answer
from gigachatAPI.utils.output_parser import parse_for_answ


def get_result_from_file(func: Callable, uploaded_file, ans_aft_que: bool, *args, dita=0) -> str:
    file_path = os.path.join('gigachatAPI/data', uploaded_file.filename)
    uploaded_file.save(file_path)

    if uploaded_file.filename.split('.')[-1] == 'zip':
        dita = 1
        unpack_path = 'gigachatAPI/data/extract_zip'
        extract_zip(file_path, unpack_path)
        os.remove(file_path)
        file_path = unpack_path

    result = func(file_path, *args, dita)

    if ans_aft_que:
        result += f'<br><br>Ответы:<br>{get_answer(file_path, parse_for_answ(result), dita, after_que=1)}'

    shutil.rmtree(file_path) if dita == 1 else os.remove(file_path)

    return result.replace('\n', '<br>')


def get_result_from_text(func: Callable, uploaded_text: str, ans_aft_que: bool, *args, dita=0) -> str:
    file_path = os.path.join('gigachatAPI/data', 'file_for_gen_que')
    with open(file_path, 'w', encoding='utf-8') as file_for_write:
        file_for_write.write(uploaded_text)

    result = func(file_path, *args, dita)

    if ans_aft_que:
        result += f'<br><br>Ответы:<br>{get_answer(file_path, parse_for_answ(result), after_que=1)}'

    os.remove(file_path)

    return result.replace('\n', '<br>')
