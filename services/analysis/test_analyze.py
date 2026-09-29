import runpy
import secrets
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace


ANALYZE_SCRIPT = Path(__file__).with_name("analyze.py")


class FakeMorpheme:
    def __init__(self, parts_of_speech, surface, normalized):
        self._parts_of_speech = parts_of_speech
        self._surface = surface
        self._normalized = normalized

    def part_of_speech(self):
        return self._parts_of_speech

    def surface(self):
        return self._surface

    def normalized_form(self):
        return self._normalized


def test_analyze_creates_wordcloud_from_selected_morpheme_forms(monkeypatch):
    split_mode_c = object()
    morphemes = [
        FakeMorpheme(("名詞", "普通名詞"), "表層名詞", "正規名詞"),
        FakeMorpheme(("動詞", "一般"), "表層動詞", "正規動詞"),
        FakeMorpheme(("形容詞", "一般"), "表層形容詞", "正規形容詞"),
        FakeMorpheme(("形状詞", "一般"), "表層形状詞", "正規形状詞"),
        FakeMorpheme(("副詞", "一般"), "表層副詞", "正規副詞"),
        FakeMorpheme(("感動詞", "一般"), "表層感動詞", "正規感動詞"),
    ]

    class FakeTokenizer:
        def tokenize(self, text, split_mode):
            self.received_text = text
            self.received_split_mode = split_mode
            return morphemes

    tokenizer_instance = FakeTokenizer()

    class FakeDictionary:
        def create(self):
            return tokenizer_instance

    sudachi_module = ModuleType("sudachipy")
    sudachi_module.dictionary = SimpleNamespace(Dictionary=FakeDictionary)
    sudachi_module.tokenizer = SimpleNamespace(
        Tokenizer=SimpleNamespace(SplitMode=SimpleNamespace(C=split_mode_c))
    )

    word_cloud_instances = []

    class FakeWordCloud:
        def __init__(self, **options):
            self.options = options
            self.generated_text = None
            self.saved_path = None
            word_cloud_instances.append(self)

        def generate(self, text):
            self.generated_text = text

        def to_file(self, path):
            self.saved_path = path

    wordcloud_module = ModuleType("wordcloud")
    wordcloud_module.WordCloud = FakeWordCloud

    config_module = ModuleType("config")
    config_module.TEXT = "入力テキスト"

    monkeypatch.setitem(sys.modules, "sudachipy", sudachi_module)
    monkeypatch.setitem(sys.modules, "wordcloud", wordcloud_module)
    monkeypatch.setitem(sys.modules, "config", config_module)
    monkeypatch.setattr(secrets, "token_urlsafe", lambda _: "fixed-output-token")

    runpy.run_path(str(ANALYZE_SCRIPT))

    assert tokenizer_instance.received_text == "入力テキスト"
    assert tokenizer_instance.received_split_mode is split_mode_c
    word_cloud = word_cloud_instances[0]
    assert word_cloud.generated_text == (
        "表層名詞 正規動詞 正規形容詞 表層形状詞 表層副詞 表層感動詞"
    )
    assert word_cloud.options == {
        "width": 1280,
        "height": 720,
        "background_color": "white",
        "font_path": "ipaexg.ttf",
    }
    assert word_cloud.saved_path == "output/fixed-output-token.png"
