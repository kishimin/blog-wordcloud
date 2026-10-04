import runpy
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace


CONFIG_SCRIPT = Path(__file__).resolve().parents[1] / "analysis" / "config.py"


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
