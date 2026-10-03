import datetime
import runpy
import secrets
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace


ANALYZE_SCRIPT = Path(__file__).resolve().parents[1] / "analyze.py"


def test_png_filename_contains_local_datetime_and_unique_token(monkeypatch):
    class FixedDateTime(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2026, 10, 1, 20, 31, 12)

    class FakeResponse:
        def __init__(self, payload):
            self.payload = payload

        def json(self):
            return self.payload

    def fake_get(url):
        if url.endswith("/sources"):
            return FakeResponse({"sources": []})
        if url.endswith("/entities/all"):
            return FakeResponse({"entities": []})
        return FakeResponse({"records": [{"body": "本文", "title": ""}]})

    class FakeWordCloud:
        saved_path = None

        def __init__(self, **options):
            pass

        def generate(self, text):
            pass

        def to_file(self, path):
            self.saved_path = path
            saved_paths.append(path)

    saved_paths = []
    sudachi_module = ModuleType("sudachipy")
    sudachi_module.dictionary = SimpleNamespace(
        Dictionary=lambda: SimpleNamespace(
            tokenizer=lambda: SimpleNamespace(tokenize=lambda *args, **kwargs: [])
        )
    )
    sudachi_module.tokenizer = SimpleNamespace(
        Tokenizer=SimpleNamespace(SplitMode=SimpleNamespace(C=object()))
    )
    wordcloud_module = ModuleType("wordcloud")
    wordcloud_module.WordCloud = FakeWordCloud
    requests_module = ModuleType("requests")
    requests_module.get = fake_get
    config_module = ModuleType("analysis.config")
    config_module.TEXT = "本文"
    config_module.SLOPE_COLLECTOR_URL = "http://collector.test"
    config_module.O_MEET_PROTECTION_WORD = ""
    config_module.R_MEET_PROTECTION_WORD = ""
    config_module.MEET_PROTECTION_WORD = ""

    monkeypatch.setattr(datetime, "datetime", FixedDateTime)
    monkeypatch.setattr(secrets, "token_urlsafe", lambda _: "fixed-output-token")
    monkeypatch.setitem(sys.modules, "sudachipy", sudachi_module)
    monkeypatch.setitem(sys.modules, "wordcloud", wordcloud_module)
    monkeypatch.setitem(sys.modules, "requests", requests_module)
    monkeypatch.setitem(sys.modules, "analysis.config", config_module)

    runpy.run_path(str(ANALYZE_SCRIPT))

    assert saved_paths == [
        str(ANALYZE_SCRIPT.parent / "output" / "20261001_203112_fixed-output-token.png")
    ]
