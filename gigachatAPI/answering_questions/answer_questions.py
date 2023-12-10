import time
from langchain.chains import LLMChain
from langchain.chat_models.gigachat import GigaChat
from gigachatAPI.config_data.config_data import *
from gigachatAPI.utils.create_prompts import create_prompt
from gigachatAPI.config_data.config import load_config, Config
from gigachatAPI.dita_case.scrap_files import get_dita_docs
from gigachatAPI.answering_questions.docs_filtration import filter_docs
from gigachatAPI.utils.split_docs import get_docs_list


def get_answer(file_path: str, question_list: list[str], dita: int) -> str:
    config: Config = load_config()

    giga: GigaChat = GigaChat(credentials=config.GIGA_CREDENTIALS, verify_ssl_certs=False)

    if dita == 1:
        split_docs = get_dita_docs(file_path)
    else:
        split_docs = get_docs_list(file_path, separator='\n', chunk_size=5000, chunk_overlap=0)

    print(f'[INFO] Всего документов: {len(split_docs)} | Длина документов:'
          f' {sum(len(i.page_content) for i in split_docs)}')

    prompt = create_prompt(get_answ_sys_prompt_path, get_answ_usr_prompt_path)

    chain = LLMChain(llm=giga, prompt=prompt)
    final_res = ''
    for q_num, que in enumerate(question_list, start=1):
        start_time = time.time()
        filtered_docs = filter_docs(split_docs, que)
        print(f'[INFO] Всего отфильтрованных документов: {len(filtered_docs)} | Длина отфильтрованных документов:'
              f' {sum(len(i.page_content) for i in filtered_docs)}')
        result = 'Ответ не найден :('
        for doc_num in range(len(filtered_docs)):
            result = chain.run(question=que, summaries=filtered_docs[doc_num])
            if (result != 'Я не могу ответить на вопрос на основе информации. Попробуйте переформулировать вопрос.'
                    and 'Для ответа на данный вопрос' not in result):
                print(f'[INFO] Ответ на вопрос №{q_num} найден в файле №{doc_num + 1} за {time.time() - start_time} секунд')
                break
            else:
                print(f'[INFO] На вопрос №{q_num} нет ответа в файле №{doc_num}')
        final_res += f'Вопрос {q_num}: {que}\nОтвет: {result}\n\n'
    return final_res

