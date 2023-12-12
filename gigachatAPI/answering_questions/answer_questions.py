import time
from langchain.chains import LLMChain
from langchain.chat_models.gigachat import GigaChat
from gigachatAPI.config_data.config_data import *
from gigachatAPI.utils.create_prompts import create_prompt
from gigachatAPI.config_data.config import load_config, Config
from gigachatAPI.dita_case.scrap_files import get_dita_docs
from gigachatAPI.dita_case.rebuild_files import change_part_size
from gigachatAPI.answering_questions.docs_filtration import filter_docs
from gigachatAPI.utils.split_docs import get_docs_list


def get_answer(file_path: str, question_list: list[str], dita: int = 0, after_que: int = 0) -> str:
    config: Config = load_config()

    giga: GigaChat = GigaChat(credentials=config.GIGA_CREDENTIALS, verify_ssl_certs=False)

    if dita == 1:
        split_docs = change_part_size(get_dita_docs(file_path))
    else:
        split_docs = get_docs_list(file_path, separator='\n', chunk_size=5000, chunk_overlap=500)

    print(f'[INFO] Всего вопросов: {len(question_list)} | Всего документов: {len(split_docs)} | Длина документов:'
          f' {sum(len(i.page_content) for i in split_docs)}')

    prompt = create_prompt(get_answ_sys_prompt_path, get_answ_usr_prompt_path)

    chain = LLMChain(llm=giga, prompt=prompt)
    final_res = ''
    for q_num, que in enumerate(question_list, start=1):
        start_time = time.time()
        filtered_docs = filter_docs(split_docs, que)
        print(f'[INFO] Документы отфильтрованы. Время: {time.time() - start_time}')
        if dita == 1:
            dita_length = sum(len(i.page_content) for i in filtered_docs)
            print(f'[INFO] Длина отфильтрованных документов: {dita_length}')
            # while dita_length > 39000:
            #     filtered_docs = filtered_docs[:-1]
            #     dita_length = sum(len(i.page_content) for i in filtered_docs)
        result = chain.run(question=que, summaries=filtered_docs)
        if after_que:
            final_res += f'{q_num}. {result}\n\n'
        else:
            final_res += f'Вопрос {q_num}: {que}\nОтвет: {result}\n\n'

        print(f'[INFO] Ответ на вопрос №{q_num} найден за {time.time() - start_time} секунд')

    return final_res
    #     print(f'[INFO] Всего отфильтрованных документов: {len(filtered_docs)} | Длина отфильтрованных документов:'
    #           f' {sum(len(i.page_content) for i in filtered_docs)}')
    #     result = ''
    #     for doc_num in range(len(filtered_docs)):
    #         result = chain.run(question=que, summaries=filtered_docs[doc_num])
    #         if (result != 'Я не могу ответить на вопрос на основе информации. Попробуйте переформулировать вопрос.'
    #                 and 'Для ответа на данный вопрос' not in result):
    #             print(f'[INFO] Ответ на вопрос №{q_num} найден в файле №{doc_num + 1} за {time.time() - start_time} секунд')
    #             break
    #         else:
    #             print(f'[INFO] На вопрос №{q_num} нет ответа в файле №{doc_num}')
    #     final_res += f'Вопрос {q_num}: {que}\nОтвет: {result}\n\n'
    # return final_res

