from pathlib import Path


def write_analysis_markdown(
    text: str, wordcloud_text: str, output_directory: Path
) -> None:
    output_directory.mkdir(parents=True, exist_ok=True)
    (output_directory / "text.md").write_text(text, encoding="utf-8")
    (output_directory / "wordcloud_text.md").write_text(
        wordcloud_text, encoding="utf-8"
    )
