import asyncio
import secrets
from types import SimpleNamespace

import analyze as image_by_entity
import analyze as image_by_frame_file


class FakeMorpheme:
    def __init__(self, part_of_speech, surface):
        self._part_of_speech = (part_of_speech,)
        self._surface = surface

    def part_of_speech(self):
        return self._part_of_speech

    def surface(self):
        return self._surface


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def json(self):
        return self.payload


class FakeWordCloud:
    instances = []

    def __init__(self, **options):
        self.options = options
        self.generated_text = None
        self.saved_path = None
        self.__class__.instances.append(self)

    def generate(self, text):
        self.generated_text = text

    def to_file(self, filename):
        self.saved_path = filename


class FakeImageContext:
    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def save(self, _):
        pass


def prepare_generation(monkeypatch, route_module, tmp_path):
    requested_urls = []

    def fake_get(url):
        requested_urls.append(url)
        if url.endswith("/sources"):
            return FakeResponse({"sources": [{"name": "Group42Unit7"}]})
        if url.endswith("/entities/all"):
            return FakeResponse({"entities": [{"name": "Example Entity"}]})
        return FakeResponse(
            {
                "records": [
                    {
                        "body": "本文 Group42Unit7 ExampleEntity 保護語 https://example.com",
                        "title": "見出し",
                    }
                ]
            }
        )

    class FakeTokenizer:
        def tokenize(self, text, mode):
            return [
                FakeMorpheme("名詞", "有効語"),
                FakeMorpheme("助詞", "除外語"),
                FakeMorpheme("名詞", "あ"),
            ]

    monkeypatch.setattr(route_module.requests, "get", fake_get)
    monkeypatch.setattr(
        route_module.dictionary,
        "Dictionary",
        lambda: SimpleNamespace(tokenizer=lambda: FakeTokenizer()),
    )
    monkeypatch.setattr(route_module, "WordCloud", FakeWordCloud)
    monkeypatch.setattr(route_module, "O_MEET_PROTECTION_WORD", "保護語")
    monkeypatch.setattr(route_module, "R_MEET_PROTECTION_WORD", "")
    monkeypatch.setattr(route_module, "MEET_PROTECTION_WORD", "")
    monkeypatch.setattr(route_module, "OUTPUT_DIRECTORY", tmp_path)
    monkeypatch.setattr(route_module.Image, "open", lambda _: FakeImageContext())
    monkeypatch.setattr(secrets, "token_urlsafe", lambda _: "test-token")

    responses = []

    def fake_file_response(path, media_type):
        response = SimpleNamespace(path=path, media_type=media_type)
        responses.append(response)
        return response

    monkeypatch.setattr(route_module.responses, "FileResponse", fake_file_response)
    FakeWordCloud.instances.clear()
    return requested_urls, responses


def test_entity_image_handler_generates_and_returns_png(monkeypatch, tmp_path):
    requested_urls, responses = prepare_generation(
        monkeypatch, image_by_entity, tmp_path
    )

    response = image_by_entity.generate_wordcloud(entity_id=19)

    assert requested_urls == [
        f"{image_by_entity.SLOPE_COLLECTOR_URL}/sources",
        f"{image_by_entity.SLOPE_COLLECTOR_URL}/entities/all",
        f"{image_by_entity.SLOPE_COLLECTOR_URL}/entities/19/records",
    ]
    wordcloud = FakeWordCloud.instances[0]
    assert wordcloud.generated_text == "有効語 Group42Unit7 ExampleEntity 保護語"
    assert wordcloud.saved_path.endswith("test-token.png")
    assert wordcloud.options["width"] == 1280
    assert wordcloud.options["height"] == 720
    assert response is responses[0]
    assert response.path == wordcloud.saved_path
    assert response.media_type == "image/png"


def test_frame_file_handler_uses_uploaded_mask_and_returns_png(monkeypatch, tmp_path):
    requested_urls, responses = prepare_generation(
        monkeypatch, image_by_frame_file, tmp_path
    )
    mask = object()

    class FakeUpload:
        async def read(self):
            return b"image-bytes"

    monkeypatch.setattr(image_by_frame_file.np, "array", lambda _: mask)

    response = asyncio.run(
        image_by_frame_file.generate_frame_file_wordcloud(
            entity_id=19, image_file=FakeUpload()
        )
    )

    assert requested_urls[-1].endswith("/entities/19/records")
    wordcloud = FakeWordCloud.instances[0]
    assert wordcloud.options["mask"] is mask
    assert wordcloud.generated_text == "有効語 Group42Unit7 ExampleEntity 保護語"
    assert response is responses[0]
    assert response.path == wordcloud.saved_path
    assert response.media_type == "image/png"
