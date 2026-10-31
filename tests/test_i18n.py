import string

from npuzzle.i18n import STRINGS, Translator
from npuzzle.settings import Settings


def fields(text: str) -> set[str]:
    return {name for _, name, _, _ in string.Formatter().parse(text) if name}


def test_every_language_has_the_same_keys_and_placeholders():
    vietnamese, english = STRINGS["vi"], STRINGS["en"]
    assert vietnamese.keys() == english.keys()
    for key in vietnamese:
        assert fields(vietnamese[key]) == fields(english[key]), key


def test_translator_fills_values_and_rejects_unknown_languages():
    assert Translator("en")("moves", count=3) == "Moves: 3"
    assert Translator("fr").language == "vi"


def test_settings_round_trip(tmp_path):
    path = tmp_path / "nested" / "settings.json"
    Settings(language="en").save(path)
    assert Settings.load(path).language == "en"


def test_missing_or_damaged_settings_use_defaults(tmp_path):
    path = tmp_path / "settings.json"
    assert Settings.load(path).language == "vi"
    path.write_text("{not json", encoding="utf-8")
    assert Settings.load(path).language == "vi"
    path.write_text('["en"]', encoding="utf-8")
    assert Settings.load(path).language == "vi"
    path.write_text('{"language": "fr"}', encoding="utf-8")
    assert Settings.load(path).language == "vi"
