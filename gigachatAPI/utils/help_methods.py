import zipfile
import os


def extract_zip(zipfile_path: str, extractes_files_path: str) -> None:
    with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
        zip_ref.extractall(extractes_files_path)


def del_dir(dir_path):
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))