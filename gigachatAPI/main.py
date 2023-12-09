from typing import Any
from random import sample
from langchain.chains import LLMChain
from langchain.chat_models.gigachat import GigaChat
from gigachatAPI.config_data.config import load_config, Config
from gigachatAPI.utils.create_prompts import create_prompt
from gigachatAPI.utils.split_docs import get_docs_list
from gigachatAPI.utils.output_parser import parse_output
from gigachatAPI.dita_case.scrap_files import get_dita_docs


def generate_questions(file_path: str, system_prompt_path: str,
                       user_prompt_path: str, cur_que_num: int, dita: int) -> Any:
    config: Config = load_config()

    giga: GigaChat = GigaChat(credentials=config.GIGA_CREDENTIALS, verify_ssl_certs=False)

    if dita == 1:
        split_docs = get_dita_docs(file_path, min_doc_length=1000)
    else:
        split_docs = get_docs_list(file_path, chunk_size=7000)

    prompt = create_prompt(system_prompt_path, user_prompt_path)

    chain = LLMChain(llm=giga, prompt=prompt)

    document_length = sum(len(i.page_content) for i in split_docs)
    max_part_doc_len = max(len(i.page_content) for i in split_docs)
    total_que_num = cur_que_num
    print(f'[INFO] Вопросов нужно: {total_que_num} | Длина дока: {document_length}')
    print(f'[INFO] Кол-во частей дока: {len(split_docs)} | Макс длина части дока: {max_part_doc_len}\n')
    if document_length > 39000:
        if len(split_docs) < cur_que_num:
            if document_length // cur_que_num >= 1000:
                split_docs = get_docs_list(file_path, chunk_size=(document_length // cur_que_num - 100))
                print(f'[INFO] Кол-во частей после перерасчета: {len(split_docs)}')
            else:
                return 'Слишком много ошибок или слишком маленький документ!'
        final_result = ''
        while True:
            for doc_part in sample(split_docs, cur_que_num):
                final_result += chain.run(num=1, text=doc_part) + '\n'
            final_result, cur_que_num = parse_output(final_result, cur_que_num, total_que_num)
            if cur_que_num:
                print(f'[INFO] Успешно сгенерировано {total_que_num - cur_que_num} вопросов')
                print(f'[INFO] Генерирую еще {cur_que_num} вопросов\n')
                continue
            print(f'[INFO] Успешно сгенерировано {total_que_num - cur_que_num} вопросов')
            print(f'[INFO] Токенов потрачено: ...хзпока...')
            return final_result
    else:
        final_result = ''
        while True:
            final_result += chain.run(num=cur_que_num, text=split_docs)
            final_result, cur_que_num = parse_output(final_result, cur_que_num, total_que_num)
            if cur_que_num:
                print(f'[INFO] Успешно сгенерировано {total_que_num - cur_que_num} вопросов')
                print(f'[INFO] Генерирую еще {cur_que_num} вопросов\n')
                continue
            print(f'[INFO] Успешно сгенерировано {total_que_num - cur_que_num} вопросов')
            print(f'[INFO] Токенов потрачено: ...хзпока...')
            return final_result
