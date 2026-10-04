from fastapi import APIRouter, responses, File, UploadFile
from pathlib import Path
from PIL import Image
from sudachipy import tokenizer
from sudachipy import dictionary
from wordcloud import WordCloud

import secrets
import requests
import re
import numpy as np
import io

from analysis.config import (
    SLOPE_COLLECTOR_URL,
    O_MEET_PROTECTION_WORD,
    R_MEET_PROTECTION_WORD,
    MEET_PROTECTION_WORD,
)
from analysis.utils.html import remove_html_tag
from analysis.utils.text_chunks import split_text_by_utf8_bytes

router = APIRouter(prefix="/images", tags=["images"])

STOP_WORDS = [
    "する",
    "なる",
    "こと",
    "ﾟ",
    "いる",
    "ござい",
    "よう",
    "なっ",
    "おり",
    "方",
    "事",
]
SERVICE_DIRECTORY = Path(__file__).resolve().parent
INPUT_DIRECTORY = SERVICE_DIRECTORY / "input"
OUTPUT_DIRECTORY = SERVICE_DIRECTORY / "output"
WORD_CLOUD_FONT_PATH = str(SERVICE_DIRECTORY / "analysis" / "assets" / "ipaexg.ttf")


OUTPUT_TOKEN_RANDOM_BYTES = 32
COLOR_MAP = "cool"
BACKGROUND_COLOR = "white"
INCLUDED_PARTS_OF_SPEECH = ("名詞", "動詞", "形容詞", "形状詞", "副詞", "感動詞")


@router.get("/{entity_id}")
def generate_wordcloud(entity_id: int):
    """
    Generate a word cloud image from the records for the requested entity.
    """
    try:
        word_cloud_width = 1280
        word_cloud_height = 720
        max_words = 100

        sources_response = requests.get(url=f"{SLOPE_COLLECTOR_URL}/sources")
        source_names = []
        for sources in sources_response.json().values():
            for source in sources:
                source_name = source["name"]
                source_names.append(source_name)
                # Do not add shorter aliases first; they could split full-name matches.
                name_without_digits = re.sub(r"\d+$", r"", source_name)
                source_names.append(name_without_digits)

        entities_response = requests.get(url=f"{SLOPE_COLLECTOR_URL}/entities/all")
        entity_names = []
        for entities in entities_response.json().values():
            for entity in entities:
                # Match names without spaces because posts may omit those spaces.
                name_without_spaces = entity["name"].replace(" ", "")
                entity_names.append(name_without_spaces)

        records_response = requests.get(
            url=f"{SLOPE_COLLECTOR_URL}/entities/{entity_id}/records"
        )

        analysis_text = ""

        for records in records_response.json().values():
            for record in records:
                body = remove_html_tag(record["body"])
                title = record["title"]
                # Keep fields separate because Sudachi could merge words across direct joins.
                analysis_text += body + " " + title + " "

        # Do not tokenize scraped "&amp;" as "amp"; it represents an ampersand, not a word.
        analysis_text = analysis_text.replace("amp;", "")

        protected_names = []

        for protected_name in source_names:
            if not protected_name:
                continue
            protected_names.extend(re.findall(re.escape(protected_name), analysis_text))
            analysis_text = analysis_text.replace(protected_name, "")

        for protected_name in entity_names:
            if not protected_name:
                continue
            protected_names.extend(re.findall(re.escape(protected_name), analysis_text))
            analysis_text = analysis_text.replace(protected_name, "")

        meet_protection_words = [
            O_MEET_PROTECTION_WORD,
            R_MEET_PROTECTION_WORD,
            MEET_PROTECTION_WORD,
        ]
        for protected_name in meet_protection_words:
            if not protected_name:
                continue
            protected_names.extend(re.findall(re.escape(protected_name), analysis_text))
            analysis_text = analysis_text.replace(protected_name, "")

        # Do not keep URLs: tokenization splits them into unrelated word cloud terms.
        url_pattern = re.compile(
            r"https?:\/\/(?:www\.)?[a-zA-Z0-9:?#/@\-._~%!$&'()*+,;=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[a-zA-Z0-9:?#/@\-._~%!$&'()*+,;=]*)"
        )
        analysis_text = re.sub(url_pattern, "", analysis_text)

        morphological_tokenizer = dictionary.Dictionary().tokenizer()

        split_mode = tokenizer.Tokenizer.SplitMode.C

        word_cloud_terms = []
        for text_chunk in split_text_by_utf8_bytes(analysis_text):
            for morpheme in morphological_tokenizer.tokenize(
                text=text_chunk, mode=split_mode
            ):
                part_of_speech = morpheme.part_of_speech()[0]
                if part_of_speech in INCLUDED_PARTS_OF_SPEECH:
                    word_cloud_terms.append(morpheme.surface())

        # Exclude single-hiragana tokens because they add little meaning to the cloud.
        single_hiragana_pattern = re.compile("^[\u3040-\u309F]$")
        word_cloud_terms = [
            term for term in word_cloud_terms if not single_hiragana_pattern.match(term)
        ]

        word_cloud_terms.extend(protected_names)

        word_cloud_text = " ".join(word_cloud_terms)

        word_cloud = WordCloud(
            width=word_cloud_width,
            height=word_cloud_height,
            background_color=BACKGROUND_COLOR,
            font_path=WORD_CLOUD_FONT_PATH,
            max_words=max_words,
            stopwords=STOP_WORDS,
            colormap=COLOR_MAP,
            collocations=False,
        )
        word_cloud.generate(word_cloud_text)

        OUTPUT_DIRECTORY.mkdir(exist_ok=True)
        output_file_token = secrets.token_urlsafe(OUTPUT_TOKEN_RANDOM_BYTES)
        file_path = str(OUTPUT_DIRECTORY / f"{output_file_token}.png")
        word_cloud.to_file(filename=file_path)

        with Image.open(file_path) as generated_image:
            generated_image.save(file_path)
        return responses.FileResponse(path=file_path, media_type="image/png")

    except Exception as e:
        raise e


@router.post("/frame-file/{entity_id}")
async def generate_frame_file_wordcloud(
    entity_id: int, image_file: UploadFile = File(...)
):
    """
    Generate a word cloud image using the uploaded frame file as its mask.
    """
    try:
        # WordCloud requires its mask as a NumPy array, so decode the uploaded bytes first.
        uploaded_image_bytes = await image_file.read()
        with Image.open(io.BytesIO(uploaded_image_bytes)) as uploaded_image:
            mask_array = np.array(uploaded_image)

        sources_response = requests.get(url=f"{SLOPE_COLLECTOR_URL}/sources")
        source_names = []
        for sources in sources_response.json().values():
            for source in sources:
                source_name = source["name"]
                source_names.append(source_name)
                # Do not add shorter aliases first; they could split full-name matches.
                name_without_digits = re.sub(r"\d+$", r"", source_name)
                source_names.append(name_without_digits)

        entities_response = requests.get(url=f"{SLOPE_COLLECTOR_URL}/entities/all")
        entity_names = []
        for entities in entities_response.json().values():
            for entity in entities:
                # Match names without spaces because posts may omit those spaces.
                name_without_spaces = entity["name"].replace(" ", "")
                entity_names.append(name_without_spaces)

        records_response = requests.get(
            url=f"{SLOPE_COLLECTOR_URL}/entities/{entity_id}/records"
        )

        analysis_text = ""

        for records in records_response.json().values():
            for record in records:
                body = remove_html_tag(record["body"])
                title = record["title"]
                # Keep fields separate because Sudachi could merge words across direct joins.
                analysis_text += body + " " + title + " "

        # Do not tokenize scraped "&amp;" as "amp"; it represents an ampersand, not a word.
        analysis_text = analysis_text.replace("amp;", "")

        protected_names = []

        for protected_name in source_names:
            if not protected_name:
                continue
            protected_names.extend(re.findall(re.escape(protected_name), analysis_text))
            analysis_text = analysis_text.replace(protected_name, "")

        for protected_name in entity_names:
            if not protected_name:
                continue
            protected_names.extend(re.findall(re.escape(protected_name), analysis_text))
            analysis_text = analysis_text.replace(protected_name, "")

        meet_protection_words = [
            O_MEET_PROTECTION_WORD,
            R_MEET_PROTECTION_WORD,
            MEET_PROTECTION_WORD,
        ]
        for protected_name in meet_protection_words:
            if not protected_name:
                continue
            protected_names.extend(re.findall(re.escape(protected_name), analysis_text))
            analysis_text = analysis_text.replace(protected_name, "")

        # Do not keep URLs: tokenization splits them into unrelated word cloud terms.
        url_pattern = re.compile(
            r"https?:\/\/(?:www\.)?[a-zA-Z0-9:?#/@\-._~%!$&'()*+,;=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[a-zA-Z0-9:?#/@\-._~%!$&'()*+,;=]*)"
        )
        analysis_text = re.sub(url_pattern, "", analysis_text)

        morphological_tokenizer = dictionary.Dictionary().tokenizer()

        split_mode = tokenizer.Tokenizer.SplitMode.C

        word_cloud_terms = []
        for text_chunk in split_text_by_utf8_bytes(analysis_text):
            for morpheme in morphological_tokenizer.tokenize(
                text=text_chunk, mode=split_mode
            ):
                part_of_speech = morpheme.part_of_speech()[0]
                if part_of_speech in INCLUDED_PARTS_OF_SPEECH:
                    word_cloud_terms.append(morpheme.surface())

        # Exclude single-hiragana tokens because they add little meaning to the cloud.
        single_hiragana_pattern = re.compile("^[\u3040-\u309F]$")
        word_cloud_terms = [
            term for term in word_cloud_terms if not single_hiragana_pattern.match(term)
        ]

        word_cloud_terms.extend(protected_names)

        word_cloud_text = " ".join(word_cloud_terms)

        word_cloud = WordCloud(
            background_color=BACKGROUND_COLOR,
            font_path=WORD_CLOUD_FONT_PATH,
            stopwords=STOP_WORDS,
            colormap=COLOR_MAP,
            collocations=False,
            mask=mask_array,
        )
        word_cloud.generate(word_cloud_text)

        OUTPUT_DIRECTORY.mkdir(exist_ok=True)
        output_file_token = secrets.token_urlsafe(OUTPUT_TOKEN_RANDOM_BYTES)
        file_path = str(OUTPUT_DIRECTORY / f"{output_file_token}.png")
        word_cloud.to_file(filename=file_path)

        with Image.open(file_path) as generated_image:
            generated_image.save(file_path)
        return responses.FileResponse(path=file_path, media_type="image/png")

    except Exception as e:
        raise e
