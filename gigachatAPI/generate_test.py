import time
from typing import Any
from random import sample
from langchain.chains import LLMChain
from langchain.chat_models.gigachat import GigaChat
from gigachatAPI.config_data.config_data import *
from gigachatAPI.config_data.config import load_config, Config
from gigachatAPI.utils.create_prompts import create_prompt
from gigachatAPI.utils.split_docs import get_docs_list
from gigachatAPI.utils.output_parser import parse_output
from gigachatAPI.utils.help_methods import get_tokens, len_yaml
from gigachatAPI.utils.split_long_elements import split_long_elements
from gigachatAPI.dita_case.scrap_files import get_dita_docs
from gigachatAPI.logs.logs import logger_info


def generate_questions(file_path: str, cur_que_num: int, dita: int) -> Any:
    config: Config = load_config()

    giga: GigaChat = GigaChat(credentials=config.GIGA_CREDENTIALS, verify_ssl_certs=False)

    start_time = time.time()

    if dita == 1:
        split_docs = get_dita_docs(file_path, min_doc_length=1000)
    else:
        split_docs = get_docs_list(file_path, chunk_size=7000)

    data_process_time = time.time() - start_time

    prompt = create_prompt(gen_que_sys_prompt_path, gen_que_usr_prompt_path)

    chain = LLMChain(llm=giga, prompt=prompt)

    document_length = sum(len(i.page_content) for i in split_docs)
    max_part_doc_len = max(len(i.page_content) for i in split_docs)

    if max_part_doc_len > 7000:
        split_docs = split_long_elements(split_docs, 7000)
        max_part_doc_len = max(len(i.page_content) for i in split_docs)

    total_que_num = cur_que_num

    logger_info.info(f'Вопросов нужно: {total_que_num} | Общая длина загруженного документа: {document_length}')
    logger_info.info(f'Кол-во частей документа: {len(split_docs)} | Максимальная длина части документа: {max_part_doc_len}\n')
    logger_info.info(f'Время обработки данных: {data_process_time} секунд\n')

    if document_length > 39000:
        if len(split_docs) < cur_que_num:
            if document_length // cur_que_num >= 1000:
                split_docs = get_docs_list(file_path, chunk_size=(document_length // cur_que_num - 100))
                logger_info.info(f'Кол-во частей после перерасчета: {len(split_docs)}')
            else:
                return 'Слишком много вопросов или слишком маленький документ!'
        final_result = ''
        token_result = 0
        gigachat_start_time = time.time()
        while True:
            for doc_part in sample(split_docs, cur_que_num):
                final_result += chain.run(num=1, text=doc_part) + '\n'
                token_result += len(doc_part.page_content)
            final_result, cur_que_num = parse_output(final_result, cur_que_num, total_que_num)
            if cur_que_num:
                logger_info.debug(f'Успешно сгенерировано {total_que_num - cur_que_num} вопросов')
                logger_info.debug(f'Генерирую еще {cur_que_num} вопросов\n')
                continue
            logger_info.debug(f'Успешно сгенерировано {total_que_num - cur_que_num} вопросов')
            tokens = get_tokens(len(final_result),
                                total_que_num * len_yaml(gen_que_sys_prompt_path),
                                token_result)
            logger_info.info(f'Токенов потрачено: {tokens}\n')
            logger_info.info(f'Время работы GigaChat: {time.time() - gigachat_start_time} секунд')
            logger_info.info(f'Общее время: {time.time() - start_time} секунд')
            return final_result
    else:
        final_result = ''
        iterations = 0
        gigachat_start_time = time.time()
        while True:
            iterations += 1
            final_result += chain.run(num=cur_que_num, text=split_docs)
            final_result, cur_que_num = parse_output(final_result, cur_que_num, total_que_num)
            if cur_que_num:
                logger_info.debug(f'Успешно сгенерировано {total_que_num - cur_que_num} вопросов')
                logger_info.debug(f'Генерирую еще {cur_que_num} вопросов\n')
                continue
            logger_info.debug(f'Успешно сгенерировано {total_que_num - cur_que_num} вопросов')
            tokens = get_tokens(len(final_result),
                                iterations * len_yaml(gen_que_sys_prompt_path),
                                iterations * document_length)
            logger_info.info(f'Токенов потрачено: {tokens}\n\n')
            logger_info.info(f'Время работы GigaChat: {time.time() - gigachat_start_time} секунд')
            logger_info.info(f'Общее время: {time.time() - start_time} секунд')
            return final_result
