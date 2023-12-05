from typing import Any
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models.gigachat import GigaChat
from config_data.config import load_config, Config
from prompt_stats.summarize_stats import get_summarize_stats
from utils.create_prompts import create_prompt
from utils.split_docs import get_docs_list


@get_summarize_stats
def use_map_reduce(file_path: str, sys_prompt_path='') -> Any:
    config: Config = load_config()

    giga: GigaChat = GigaChat(credentials=config.GIGA_CREDENTIALS, verify_ssl_certs=False)

    split_docs = get_docs_list(file_path, separator='\n', chunk_size=5000, chunk_overlap=500)

    map_prompt = create_prompt(sys_prompt_path)
    chain = load_summarize_chain(giga, chain_type="map_reduce")
    res = chain.run(split_docs)

    return res


