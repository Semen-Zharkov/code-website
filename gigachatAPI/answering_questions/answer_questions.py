import time
from langchain.chains import LLMChain
from langchain.chains import RetrievalQA
from langchain.chat_models.gigachat import GigaChat
from gigachatAPI.config_data.config_data import *
from gigachatAPI.utils.create_prompts import create_prompt
from gigachatAPI.config_data.config import load_config, Config
from gigachatAPI.dita_case.scrap_files import get_dita_docs
from gigachatAPI.answering_questions.docs_filtration import filter_docs
from gigachatAPI.utils.split_docs import get_docs_list
from gigachatAPI.utils.help_methods import get_tokens
from gigachatAPI.logs.logs import logger_info


def get_answer(file_path: str, question_list: list[str], dita: int = 0, after_que: bool = False) -> str:
    config: Config = load_config()

    giga: GigaChat = GigaChat(credentials=config.GIGA_CREDENTIALS, verify_ssl_certs=False)

    start_time = time.time()

    if dita == 1:
        split_docs = get_dita_docs(file_path, chunk_size=10000)
        func = filter_docs
        out_files_num = 1
    else:
        split_docs = get_docs_list(file_path, separator='\n', chunk_size=25000)
        func = filter_docs
        out_files_num = 1

    data_process_time = time.time() - start_time

    logger_info.info(f'Всего вопросов: {len(question_list)} | Всего документов: {len(split_docs)} | Длина документов:'
                     f' {sum(len(i.page_content) for i in split_docs)}\n')
    logger_info.info(f'Время обработки данных: {data_process_time} секунд\n')

    # prompt = create_prompt(get_answ_sys_prompt_path, get_answ_usr_prompt_path)
    tokens_result = 0
    final_res = ''
    for q_num, que in enumerate(question_list, start=1):
        dita_length = 0
        question_start_time = time.time()
        filtered_docs, retriever = func(split_docs, que, out_files_num=out_files_num)
        logger_info.info(f'Время работы Chroma для вопроса №{q_num}: {time.time() - question_start_time} секунд')
        chain = RetrievalQA.from_chain_type(llm=giga, retriever=retriever.as_retriever())
        gigachat_start_time = time.time()
        if dita == 1:
            dita_length = sum(len(i.page_content) for i in filtered_docs)
            logger_info.info(f'Длина отфильтрованных документов: {dita_length}')
        # result = chain.run(question=que, summaries=filtered_docs)
        qa_chain = chain({"query": que})
        result = qa_chain['result']
        logger_info.info(f'Время работы GigaChat для вопроса №{q_num}: {time.time() - gigachat_start_time} секунд')
        if after_que:
            final_res += f'{q_num}. {result}\n\n'
        else:
            final_res += f'Вопрос {q_num}: {que}\nОтвет: {result}\n\n'
        tokens = get_tokens(dita_length, len(result))
        tokens_result += tokens
        logger_info.info(f'Потраченные Токены для вопроса №{q_num}: {tokens}')
        logger_info.info(f'Общее время для вопроса №{q_num}: {time.time() - question_start_time} секунд\n')
    logger_info.info(f'Общее количество потраченных Токенов: {tokens_result}')
    logger_info.info(f'Общее время: {time.time() - start_time}')
    return final_res
