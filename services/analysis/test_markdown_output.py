from markdown_output import write_analysis_markdown


def test_write_analysis_markdown_saves_both_text_values_as_utf8(
    tmp_path,
):
    text = "見出し #1\n本文 🙂"
    wordcloud_text = "解析 語彙"

    write_analysis_markdown(text, wordcloud_text, tmp_path)

    assert (tmp_path / "text.md").read_text(encoding="utf-8") == text
    assert (tmp_path / "wordcloud_text.md").read_text(encoding="utf-8") == (
        wordcloud_text
    )


def test_write_analysis_markdown_creates_output_directory(tmp_path):
    output_directory = tmp_path / "output"

    write_analysis_markdown("source", "tokens", output_directory)

    assert (output_directory / "text.md").read_text(encoding="utf-8") == "source"
    assert (output_directory / "wordcloud_text.md").read_text(encoding="utf-8") == (
        "tokens"
    )
