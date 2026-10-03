SUDACHI_MAX_INPUT_BYTES = 49_149
TEXT_BOUNDARIES = frozenset("。！？.!?\r\n")


def split_text_by_utf8_bytes(
    text: str, max_bytes: int = SUDACHI_MAX_INPUT_BYTES
) -> list[str]:
    if max_bytes < 1:
        raise ValueError("max_bytes must be positive")

    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = start
        last_boundary = start
        chunk_bytes = 0

        while end < len(text):
            character_bytes = len(text[end].encode("utf-8"))
            if character_bytes > max_bytes:
                raise ValueError("max_bytes is smaller than a character's UTF-8 size")
            if chunk_bytes + character_bytes > max_bytes:
                break

            chunk_bytes += character_bytes
            end += 1
            if text[end - 1] in TEXT_BOUNDARIES:
                last_boundary = end

        if end < len(text) and last_boundary > start:
            end = last_boundary

        chunks.append(text[start:end])
        start = end

    return chunks
