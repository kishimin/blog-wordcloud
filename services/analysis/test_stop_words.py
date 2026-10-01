import runpy
import sys
from pathlib import Path
from types import ModuleType

import requests
from sudachipy import dictionary
from wordcloud import WordCloud


ANALYZE_SCRIPT = Path(__file__).with_name("analyze.py")


def test_analysis_excludes_halfwidth_semivoiced_mark_from_wordcloud(monkeypatch):
    class FakeMorpheme:
        def __init__(self, surface):
            self._surface = surface

        def part_of_speech(self):
            return ("名詞",)

        def surface(self):
            return self._surface

    class FakeTokenizer:
        def tokenize(self, text, mode):
            return [FakeMorpheme("ﾟ"), FakeMorpheme("有効語")]

    class FakeDictionary:
        def create(self):
            return FakeTokenizer()

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

    config_module = ModuleType("config")
    config_module.SLOPE_COLLECTOR_URL = "http://collector.test"
    monkeypatch.setitem(sys.modules, "config", config_module)
    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr(dictionary, "Dictionary", FakeDictionary)
    monkeypatch.setattr(WordCloud, "to_file", lambda self, path: None)

    analysis = runpy.run_path(str(ANALYZE_SCRIPT))

    assert "ﾟ" not in analysis["word_cloud"].words_
    assert "有効語" in analysis["word_cloud"].words_
