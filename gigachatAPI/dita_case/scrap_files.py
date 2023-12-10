import fnmatch
import os
from langchain.schema import Document
from gigachatAPI.utils.help_methods import get_doc_length
from langchain.document_loaders import TextLoader


def get_dita_docs(dita_path: str, min_doc_length=0) -> list[Document]:

    def func(directory_path):
        dit = {}
        for root, dirs, files in os.walk(directory_path):
            for file in fnmatch.filter(files, '*.dita'):
                file_path = os.path.join(root, file)
                dit[file_path] = get_doc_length(file_path)
        return dit

    dita_dict = func(dita_path)
    path_list_less = [i for i, j in dita_dict.items() if j > min_doc_length]
    path_list = list(dita_dict.keys())

    docs = TextLoader(path_list[0], encoding='utf-8').load()
    split_docs = [TextLoader(pt, encoding='utf-8').load() for pt in path_list_less[1:]]
    for i in split_docs:
        docs += i

    return docs
