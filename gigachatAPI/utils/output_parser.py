import re


def parse_output(text: str):
    pattern = re.compile(r"(\d+\. .*?\n(a\) .*?\n|b\) .*?\n|c\) .*?\n|d\) .*?\n)+)")

    matches = pattern.findall(text)
    result = ''
    for num, i in enumerate(matches, start=1):
        result += f'{num}{i[0][i[0].index("."):]}'
        if i != matches[-1]:
            result += '\n'
    return result
