from langchain.schema import Document


def change_part_size(split_docs: list[Document]) -> list[Document]:
    very_long_string = ''.join(list(map(lambda x: x.page_content, split_docs)))
    chunk_size = 5000
    result_list = [very_long_string[i:i + chunk_size] for i in range(0, len(very_long_string), chunk_size)]
    docs = [
        Document(
            page_content=split,
        )
        for split in result_list
    ]
    return docs
