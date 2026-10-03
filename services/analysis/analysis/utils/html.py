import re


def remove_html_tag(text: str):
    return re.sub(re.compile("<.*?>"), "", text)
