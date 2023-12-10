import os
import shutil
from typing import Callable
from flask import Flask, render_template, request, jsonify
from gigachatAPI.utils.help_methods import *


def get_result_from_file(func: Callable, uploaded_file, *args, dita=0) -> str:
    file_path = os.path.join('gigachatAPI/data', uploaded_file.filename)
    uploaded_file.save(file_path)
    print(f'{uploaded_file.filename} сохранен')

    if uploaded_file.filename.split('.')[-1] == 'zip':
        dita = 1
        unpack_path = 'gigachatAPI/data/extract_zip'
        extract_zip(file_path, unpack_path)
        os.remove(file_path)
        file_path = unpack_path

    result = func(file_path, *args, dita)

    shutil.rmtree(file_path) if dita == 1 else os.remove(file_path)
    print(f'{uploaded_file.filename} удален')

    return result


def get_result_from_text(func: Callable, uploaded_text: str, *args, dita=0) -> str:
    file_path = os.path.join('gigachatAPI/data', 'file_for_gen_que')
    with open(file_path, 'w', encoding='utf-8') as file_for_write:
        file_for_write.write(uploaded_text)

    result = func(file_path, *args, dita)
    os.remove(file_path)

    return result
