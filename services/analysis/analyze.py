from pathlib import Path
from datetime import datetime

from sudachipy import tokenizer
from sudachipy import dictionary
from wordcloud import WordCloud

import secrets
import requests
import re

from config import SLOPE_COLLECTOR_URL
from markdown_output import write_analysis_markdown
from text_chunks import split_text_by_utf8_bytes


def remove_html_tag(text: str):
    return re.sub(re.compile("<.*?>"), "", text)


ENTITY_ID = 10
STOP_WORDS = [
    "し",
    "する",
    "なる",
    "こと",
    "ﾟ",
    "いる",
    "ござい",
    "https",
    "よう",
    "なっ",
    "おり",
    "方",
    "日",
    "amp",
    "事",
    "com",
]
ANALYSIS_DIRECTORY = Path(__file__).resolve().parent
OUTPUT_DIRECTORY = ANALYSIS_DIRECTORY / "output"
font_path = str(ANALYSIS_DIRECTORY / "ipaexg.ttf")


WORD_CLOUD_WIDTH = 1280
WORD_CLOUD_HEIGHT = 720
OUTPUT_TOKEN_RANDOM_BYTES = 32
COLOR_MAP = "cool"
MAX_WORDS = 100
BACKGROUND_COLOR = "white"

request_sources = requests.get(url=f"{SLOPE_COLLECTOR_URL}/sources")
request_sources_dict = request_sources.json()
source_name_list = []
for x in request_sources_dict:
    items = request_sources_dict[x]
    for count in range(len(items)):
        source = items[count]
        name = source["name"]
        source_name_list.append(name)
        # Posts often use the source name without its numeric suffix.
        omission_name = re.sub(r"\d+", r"", name)
        source_name_list.append(omission_name)

request_all_entities = requests.get(url=f"{SLOPE_COLLECTOR_URL}/entities/all")
request_all_entities_dict = request_all_entities.json()

all_entity_name_list = []
for x in request_all_entities_dict:
    items = request_all_entities_dict[x]
    for count in range(len(items)):
        entity = items[count]
        # Posts often omit the spaces in entity names.
        full_name = entity["name"].replace(" ", "")
        all_entity_name_list.append(full_name)

request = requests.get(url=f"{SLOPE_COLLECTOR_URL}/entities/{ENTITY_ID}/records")

text = ""

request_dict = request.json()
for x in request_dict:
    items = request_dict[x]
    for count in range(len(items)):
        content = items[count]
        body = remove_html_tag(content["body"])
        title = content["title"]
        text += body + title

protection_words = []

for name in source_name_list:
    if not name:
        continue
    protection_words.extend(re.findall(re.escape(name), text))
    text = text.replace(name, "")

for name in all_entity_name_list:
    if not name:
        continue
    protection_words.extend(re.findall(re.escape(name), text))
    text = text.replace(name, "")


morphological_tokenizer = dictionary.Dictionary().create()

split_mode = tokenizer.Tokenizer.SplitMode.C

wordcloud_terms = []
for text_chunk in split_text_by_utf8_bytes(text):
    for morpheme in morphological_tokenizer.tokenize(text=text_chunk, mode=split_mode):
        part_of_speech = morpheme.part_of_speech()[0]
        if part_of_speech in ("名詞", "動詞", "形容詞", "形状詞", "副詞", "感動詞"):
            wordcloud_terms.append(morpheme.surface())

# A single hiragana character carries little meaning in the word cloud.
kana_re = re.compile("^[\u3040-\u309F]$")
wordcloud_terms = [w for w in wordcloud_terms if not kana_re.match(w)]

wordcloud_terms.extend(protection_words)

wordcloud_text = " ".join(wordcloud_terms)

word_cloud = WordCloud(
    width=WORD_CLOUD_WIDTH,
    height=WORD_CLOUD_HEIGHT,
    background_color=BACKGROUND_COLOR,
    font_path=font_path,
    max_words=MAX_WORDS,
    stopwords=STOP_WORDS,
    colormap=COLOR_MAP,
    collocations=False,
)
word_cloud.generate(wordcloud_text)

write_analysis_markdown(text, wordcloud_text, OUTPUT_DIRECTORY)

OUTPUT_DIRECTORY.mkdir(exist_ok=True)
output_file_token = secrets.token_urlsafe(OUTPUT_TOKEN_RANDOM_BYTES)
output_timestamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
word_cloud.to_file(
    str(OUTPUT_DIRECTORY / f"{output_timestamp}_{output_file_token}.png")
)
