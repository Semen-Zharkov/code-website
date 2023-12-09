from functools import wraps
import os
import csv
import yaml
import time


def is_format_followed(string: str, que_num: int) -> tuple[bool, bool]:
    string_list = string.split('\n\n')
    string_list = list(filter(None, map(lambda x: list(filter(None, x.split('\n'))), string_list)))
    is_corr_num = True if len(string_list) == que_num else False

    for enum, que in enumerate(string_list, start=1):
        for i in que:
            if i[0] != str(enum) and i[0] not in 'abcd':
                return False, is_corr_num
    return True, is_corr_num


def read_yaml(path_yaml: str) -> str:
    if not path_yaml:
        return '-'
    with open(path_yaml, encoding='utf-8') as fh:
        dict_data = yaml.safe_load(fh)
        template = dict_data['template']
        return template


def get_doc_length(path_doc: str) -> int:
    with open(path_doc, 'r', encoding='utf-8') as file:
        return len(file.read())


def get_tokens(s1: str, s2: str, s3: str, ln: int) -> int:
    sm = sum(map(len, [s1, s2, s3])) + ln
    return (sm // 3 + sm // 4) // 2


def get_statistics():
    def func_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sys_templ = read_yaml(args[1])
            usr_templ = read_yaml(args[2])
            length = get_doc_length(args[0])
            start_time = time.time()
            res = func(*args, **kwargs)
            res_time = time.time() - start_time
            tokens = get_tokens(usr_templ, sys_templ, res, length)
            if not os.path.isfile('prompt_stats/statistics.csv'):
                with open('prompt_stats/statistics.csv', 'w', encoding='cp1251') as file:
                    file.write(''.join(['file_name;prompt_name;document_length;format_followed;',
                                       'question_number_correct;lead_time;spent_tokens;sys_prompt_template;',
                                        'usr_prompt_template;returned\n']))
            with open('prompt_stats/statistics.csv', 'a+', encoding='cp1251', newline='') as stats:
                writer = csv.writer(stats, delimiter=';')
                writer.writerow(
                    [args[0], args[1], length, *is_format_followed(res, args[3]),
                     res_time, tokens, sys_templ, usr_templ, res]
                )
            return res

        return wrapper
    return func_decorator
