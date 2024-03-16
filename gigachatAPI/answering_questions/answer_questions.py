import time

from langchain.chains import RetrievalQA
from langchain.chat_models.gigachat import GigaChat
from gigachatAPI.config_data.config_data import *
from gigachatAPI.prompts.qna_system_temp import custom_rag_prompt
from langchain import hub
from gigachatAPI.config_data.config import load_config, Config
from gigachatAPI.dita_case.scrap_files import get_dita_docs
from gigachatAPI.answering_questions.docs_filtration import filter_docs
from gigachatAPI.utils.split_docs import get_docs_list
from gigachatAPI.utils.help_methods import get_tokens
from gigachatAPI.logs.logs import logger_info
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def get_answer(file_path: str, question_list: list[str], dita: int = 0, after_que: bool = False) -> str:
    config: Config = load_config()

    giga: GigaChat = GigaChat(credentials=config.GIGA_CREDENTIALS, verify_ssl_certs=False)

    start_time = time.time()

    if dita == 1:
        split_docs = get_dita_docs(file_path, chunk_size=10000)
    else:
        split_docs = get_docs_list(file_path, separator='\n', chunk_size=10000)

    data_process_time = time.time() - start_time

    logger_info.info(f'Всего вопросов: {len(question_list)} | Всего документов: {len(split_docs)} | Длина документов:'
                     f' {sum(len(i.page_content) for i in split_docs)}\n')
    logger_info.info(f'Время обработки данных: {data_process_time} секунд\n')

    # prompt = hub.pull("rlm/rag-prompt")

    tokens_result = 0

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    final_res = ''
    for q_num, que in enumerate(question_list, start=1):
        dita_length = 0
        question_start_time = time.time()
        filtered_docs, retriever = filter_docs(split_docs, que, out_files_num=1)
        logger_info.info(f'Время работы Chroma для вопроса №{q_num}: {time.time() - question_start_time} секунд')

        # rag_chain = (
        #         {"context": retriever | format_docs, "question": RunnablePassthrough()}
        #         | custom_rag_prompt
        #         | giga
        #         | StrOutputParser()
        # )
        chain = RetrievalQA.from_chain_type(
            llm=giga,
            # chain_type="stuff",
            retriever=retriever.as_retriever(
                # search_type="similarity",
                search_kwargs={"k": 1}
            ),
            # verbose=True,
            chain_type_kwargs={
                # "verbose": True,
                "prompt": custom_rag_prompt
            }
        )

        gigachat_start_time = time.time()
        if dita == 1:
            dita_length = sum(len(i.page_content) for i in filtered_docs)
            logger_info.info(f'Длина отфильтрованных документов: {dita_length}')

        # result = rag_chain.invoke(que)
        qa_chain = chain.invoke({"query": que})
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
