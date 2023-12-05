from typing import Any
from random import randint
from langchain.chains import LLMChain
from langchain.chat_models.gigachat import GigaChat
from gigachatAPI.config_data.config import load_config, Config
from gigachatAPI.utils.create_prompts import create_prompt
from gigachatAPI.utils.split_docs import get_docs_list
from gigachatAPI.utils.output_parser import parse_output
from gigachatAPI.dita_case.scrap_files import get_dita_docs
from gigachatAPI.answering_questions.answer_questions import get_answer


def generate_questions(file_path: str, que_num: int, system_prompt_path: str,
                       user_prompt_path: str = '', dita: int = '0') -> Any:
    config: Config = load_config()

    giga: GigaChat = GigaChat(credentials=config.GIGA_CREDENTIALS, verify_ssl_certs=False)

    if dita == 1:
        split_docs = get_dita_docs(file_path, min_doc_length=10000)
    else:
        split_docs = get_docs_list(file_path)

    prompt = create_prompt(system_prompt_path, user_prompt_path)

    chain = LLMChain(llm=giga, prompt=prompt)

    if sum(len(i.page_content) for i in split_docs) > 39000:
        res = ''
        for i in range(que_num):
            rnd = randint(0, len(split_docs) - 1)
            res += chain.run(num=1, text=split_docs[rnd]) + '\n\n'
        return res
    else:
        result = chain.run(num=que_num, text=split_docs)
        return parse_output(result)

# if __name__ == '__main__':
#     SYS_PROMPT_PATH = 'prompts/generate_question_prompt.yaml'
#     USR_PROMPT_PATH = ''
#     PATH = 'data/crime6.txt'
#     questions_number = 5
#     print(generate_questions(PATH, SYS_PROMPT_PATH, USR_PROMPT_PATH, questions_number, dita=0))
#
#     """Блок ответов на вопросы"""
# for answer in get_answer('data/crime6.txt', 'prompts/qna_system.yaml',
#                          'prompts/qna_user.yaml', questions_for_crimetxt, dita=0):
#     print(answer)
