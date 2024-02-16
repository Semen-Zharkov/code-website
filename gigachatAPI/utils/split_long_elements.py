from langchain.schema import Document


def split_long_elements(input_list: list[Document], max_length: int) -> list[Document]:
    input_list = list(map(lambda x: x.page_content, input_list))
    result_list = []

    for string in input_list:
        if len(string) > max_length:
            num_splits = (len(string) - 1) // max_length + 1
            split_length = (len(string) - 1) // num_splits + 1
            split_strings = [string[i:i+split_length] for i in range(0, len(string), split_length)]
            result_list.extend(split_strings)
        else:
            result_list.append(string)

    result_list = list(map(lambda x: Document(page_content=x), result_list))
    return result_list
