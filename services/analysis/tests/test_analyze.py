import runpy
import secrets
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace


ANALYZE_SCRIPT = Path(__file__).resolve().parents[1] / "analyze.py"
CONFIG_SCRIPT = Path(__file__).resolve().parents[1] / "analysis" / "config.py"


class FakeMorpheme:
    def __init__(self, parts_of_speech, surface):
        self._parts_of_speech = parts_of_speech
        self._surface = surface

    def part_of_speech(self):
        return self._parts_of_speech

    def surface(self):
        return self._surface


def test_analyze_creates_wordcloud_from_surface_forms(monkeypatch):
    split_mode_c = object()
    morphemes = [
        FakeMorpheme(("名詞", "普通名詞"), "表層名詞"),
        FakeMorpheme(("動詞", "一般"), "表層動詞"),
        FakeMorpheme(("形容詞", "一般"), "表層形容詞"),
        FakeMorpheme(("形状詞", "一般"), "表層形状詞"),
        FakeMorpheme(("副詞", "一般"), "表層副詞"),
        FakeMorpheme(("感動詞", "一般"), "表層感動詞"),
    ]

    class FakeTokenizer:
        received_texts = []

        def tokenize(self, text, mode):
            self.received_texts.append(text)
            self.received_split_mode = mode
            return morphemes

    tokenizer_instance = FakeTokenizer()

    class FakeDictionary:
        def tokenizer(self):
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

    config_module = ModuleType("analysis.config")
    config_module.SLOPE_COLLECTOR_URL = "http://collector.test"
    config_module.O_MEET_PROTECTION_WORD = "keep-me"
    config_module.R_MEET_PROTECTION_WORD = ""
    config_module.MEET_PROTECTION_WORD = ""

    analysis_text = "あ" * 20_000

    class FakeResponse:
        def __init__(self, payload):
            self.payload = payload

        def json(self):
            return self.payload

    requested_urls = []

    def fake_get(url):
        requested_urls.append(url)
        if url.endswith("/sources"):
            return FakeResponse({"sources": [{"name": "Group46Unit7"}]})
        if url.endswith("/entities/all"):
            return FakeResponse({"entities": []})
        return FakeResponse(
            {
                "records": [
                    {
                        "body": analysis_text
                        + "Group46Unit keep-me https://example.com/path",
                        "title": "見出し",
                    },
                    {"body": "次本文", "title": "次見出し"},
                ]
            }
        )

    requests_module = ModuleType("requests")
    requests_module.get = fake_get

    monkeypatch.setitem(sys.modules, "sudachipy", sudachi_module)
    monkeypatch.setitem(sys.modules, "wordcloud", wordcloud_module)
    monkeypatch.setitem(sys.modules, "analysis.config", config_module)
    monkeypatch.setitem(sys.modules, "requests", requests_module)
    monkeypatch.setattr(secrets, "token_urlsafe", lambda _: "fixed-output-token")

    runpy.run_path(str(ANALYZE_SCRIPT))

    assert requested_urls == [
        "http://collector.test/sources",
        "http://collector.test/entities/all",
        "http://collector.test/entities/8/records",
    ]
    assert len(tokenizer_instance.received_texts) > 1
    assert "".join(tokenizer_instance.received_texts).split() == [
        analysis_text,
        "見出し",
        "次本文",
        "次見出し",
    ]
    assert all(
        len(chunk.encode("utf-8")) <= 49_149
        for chunk in tokenizer_instance.received_texts
    )
    assert tokenizer_instance.received_split_mode is split_mode_c
    word_cloud = word_cloud_instances[0]
    selected_terms = "表層名詞 表層動詞 表層形容詞 表層形状詞 表層副詞 表層感動詞"
    assert word_cloud.generated_text == " ".join(
        [selected_terms] * len(tokenizer_instance.received_texts)
        + ["Group46Unit", "keep-me"]
    )
    assert word_cloud.options == {
        "width": 1280,
        "height": 720,
        "background_color": "white",
        "font_path": str(ANALYZE_SCRIPT.parent / "analysis" / "assets" / "ipaexg.ttf"),
        "max_words": 100,
        "stopwords": [
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
        ],
        "colormap": "cool",
        "collocations": False,
    }
    assert Path(word_cloud.saved_path).parent == ANALYZE_SCRIPT.parent / "output"
    assert Path(word_cloud.saved_path).name.endswith("_fixed-output-token.png")


def test_config_loads_collector_url_from_its_directory(monkeypatch):
    dotenv_paths = []

    def fake_load_dotenv(dotenv_path=None):
        dotenv_paths.append(dotenv_path)
        monkeypatch.setenv("SLOPE_COLLECTOR_URL", "http://collector.test")
        monkeypatch.setenv("O_MEET_PROTECTION_WORD", "sample-one")
        monkeypatch.setenv("R_MEET_PROTECTION_WORD", "sample-two")
        monkeypatch.setenv("MEET_PROTECTION_WORD", "sample-three")

    dotenv_module = ModuleType("dotenv")
    dotenv_module.load_dotenv = fake_load_dotenv
    monkeypatch.setitem(sys.modules, "dotenv", dotenv_module)
    monkeypatch.delenv("SLOPE_COLLECTOR_URL", raising=False)

    config_namespace = runpy.run_path(str(CONFIG_SCRIPT))

    assert config_namespace["SLOPE_COLLECTOR_URL"] == "http://collector.test"
    assert config_namespace["O_MEET_PROTECTION_WORD"] == "sample-one"
    assert config_namespace["R_MEET_PROTECTION_WORD"] == "sample-two"
    assert config_namespace["MEET_PROTECTION_WORD"] == "sample-three"
    assert dotenv_paths == [CONFIG_SCRIPT.parents[1] / ".env"]
