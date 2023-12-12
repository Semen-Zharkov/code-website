import zipfile
import yaml
import os


def extract_zip(zipfile_path: str, extractes_files_path: str) -> None:
    with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
        zip_ref.extractall(extractes_files_path)


def get_doc_length(path_doc: str) -> int:
    with open(path_doc, 'r', encoding='utf-8') as file:
        return len(file.read())


def get_tokens(s1: int, s2: int, ln: int) -> int:
    sm = sum((s1, s2, ln))
    return (sm // 3 + sm // 4) // 2


def len_yaml(path_yaml: str) -> int:
    with open(path_yaml, encoding='utf-8') as fh:
        dict_data = yaml.safe_load(fh)
        result = sum(map(len, filter(None, dict_data.values())))
        return result
