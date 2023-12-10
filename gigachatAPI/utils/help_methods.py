import zipfile


def extract_zip(zipfile_path: str, extractes_files_path: str) -> None:
    with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
        zip_ref.extractall(extractes_files_path)


def get_doc_length(path_doc: str) -> int:
    with open(path_doc, 'r', encoding='utf-8') as file:
        return len(file.read())
