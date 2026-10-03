import pytest

from analysis.utils.text_chunks import split_text_by_utf8_bytes


def test_split_text_by_utf8_bytes_preserves_text_and_respects_byte_limit():
    text = "aあ🙂b" * 4

    chunks = split_text_by_utf8_bytes(text, max_bytes=8)

    assert "".join(chunks) == text
    assert all(len(chunk.encode("utf-8")) <= 8 for chunk in chunks)
    assert all(chunk for chunk in chunks)


def test_split_text_by_utf8_bytes_keeps_multibyte_characters_intact():
    chunks = split_text_by_utf8_bytes("あ🙂", max_bytes=4)

    assert chunks == ["あ", "🙂"]


def test_split_text_by_utf8_bytes_prefers_sentence_boundaries():
    chunks = split_text_by_utf8_bytes("前の文。次の文の続き", max_bytes=15)

    assert chunks[0] == "前の文。"
    assert "".join(chunks) == "前の文。次の文の続き"


def test_split_text_by_utf8_bytes_rejects_limit_smaller_than_one_character():
    with pytest.raises(ValueError, match="max_bytes"):
        split_text_by_utf8_bytes("あ", max_bytes=2)


def test_split_text_by_utf8_bytes_rejects_non_positive_limit():
    with pytest.raises(ValueError, match="max_bytes"):
        split_text_by_utf8_bytes("text", max_bytes=0)
