from sudachipy import tokenizer
from sudachipy import dictionary
from wordcloud import WordCloud

import secrets

from config import TEXT


WORD_CLOUD_WIDTH = 1280
WORD_CLOUD_HEIGHT = 720
OUTPUT_TOKEN_RANDOM_BYTES = 32

morphological_tokenizer = dictionary.Dictionary().create()

split_mode = tokenizer.Tokenizer.SplitMode.C

part_of_speech_rules = {
    "名詞": False,
    "動詞": True,
    "形容詞": True,
    "形状詞": False,
    "副詞": False,
    "感動詞": False,
}

wordcloud_terms = []
for morpheme in morphological_tokenizer.tokenize(TEXT, split_mode):
    for part_of_speech_name, use_normalized_form in part_of_speech_rules.items():
        if part_of_speech_name in morpheme.part_of_speech():
            if use_normalized_form:
                wordcloud_terms.append(morpheme.normalized_form())
            else:
                wordcloud_terms.append(morpheme.surface())

wordcloud_text = " ".join(wordcloud_terms)

font_path = "ipaexg.ttf"
word_cloud = WordCloud(
    width=WORD_CLOUD_WIDTH,
    height=WORD_CLOUD_HEIGHT,
    background_color="white",
    font_path=font_path,
)
word_cloud.generate(wordcloud_text)
output_file_token = secrets.token_urlsafe(OUTPUT_TOKEN_RANDOM_BYTES)
word_cloud.to_file(f"output/{output_file_token}.png")
