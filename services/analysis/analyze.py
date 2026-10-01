from pathlib import Path
from datetime import datetime

from sudachipy import tokenizer
from sudachipy import dictionary
from wordcloud import WordCloud

import secrets
import requests
import re

from analysis.config import SLOPE_COLLECTOR_URL
from analysis.text_chunks import split_text_by_utf8_bytes


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
SERVICE_DIRECTORY = Path(__file__).resolve().parent
OUTPUT_DIRECTORY = SERVICE_DIRECTORY / "output"
WORD_CLOUD_FONT_PATH = str(SERVICE_DIRECTORY / "analysis" / "assets" / "ipaexg.ttf")


WORD_CLOUD_WIDTH = 1280
WORD_CLOUD_HEIGHT = 720
OUTPUT_TOKEN_RANDOM_BYTES = 32
COLOR_MAP = "cool"
MAX_WORDS = 100
BACKGROUND_COLOR = "white"
INCLUDED_PARTS_OF_SPEECH = ("名詞", "動詞", "形容詞", "形状詞", "副詞", "感動詞")

sources_response = requests.get(url=f"{SLOPE_COLLECTOR_URL}/sources")
source_names = []
for sources in sources_response.json().values():
    for source in sources:
        source_name = source["name"]
        source_names.append(source_name)
        # Posts often use the source name without its numeric suffix.
        name_without_digits = re.sub(r"\d+", r"", source_name)
        source_names.append(name_without_digits)

entities_response = requests.get(url=f"{SLOPE_COLLECTOR_URL}/entities/all")

entity_names = []
for entities in entities_response.json().values():
    for entity in entities:
        # Posts often omit the spaces in entity names.
        name_without_spaces = entity["name"].replace(" ", "")
        entity_names.append(name_without_spaces)

records_response = requests.get(
    url=f"{SLOPE_COLLECTOR_URL}/entities/{ENTITY_ID}/records"
)

analysis_text = ""

for records in records_response.json().values():
    for record in records:
        body = remove_html_tag(record["body"])
        title = record["title"]
        analysis_text += body + title

protected_names = []

for name in source_names:
    if not name:
        continue
    protected_names.extend(re.findall(re.escape(name), analysis_text))
    analysis_text = analysis_text.replace(name, "")

for name in entity_names:
    if not name:
        continue
    protected_names.extend(re.findall(re.escape(name), analysis_text))
    analysis_text = analysis_text.replace(name, "")


morphological_tokenizer = dictionary.Dictionary().create()

split_mode = tokenizer.Tokenizer.SplitMode.C

wordcloud_terms = []
for text_chunk in split_text_by_utf8_bytes(analysis_text):
    for morpheme in morphological_tokenizer.tokenize(text=text_chunk, mode=split_mode):
        part_of_speech = morpheme.part_of_speech()[0]
        if part_of_speech in INCLUDED_PARTS_OF_SPEECH:
            wordcloud_terms.append(morpheme.surface())

# A single hiragana character carries little meaning in the word cloud.
kana_re = re.compile("^[\u3040-\u309F]$")
wordcloud_terms = [w for w in wordcloud_terms if not kana_re.match(w)]

wordcloud_terms.extend(protected_names)

wordcloud_text = " ".join(wordcloud_terms)

word_cloud = WordCloud(
    width=WORD_CLOUD_WIDTH,
    height=WORD_CLOUD_HEIGHT,
    background_color=BACKGROUND_COLOR,
    font_path=WORD_CLOUD_FONT_PATH,
    max_words=MAX_WORDS,
    stopwords=STOP_WORDS,
    colormap=COLOR_MAP,
    collocations=False,
)
word_cloud.generate(wordcloud_text)

OUTPUT_DIRECTORY.mkdir(exist_ok=True)
output_file_token = secrets.token_urlsafe(OUTPUT_TOKEN_RANDOM_BYTES)
output_timestamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
word_cloud.to_file(
    str(OUTPUT_DIRECTORY / f"{output_timestamp}_{output_file_token}.png")
)
