"""User settings, stored as JSON in the per-user configuration folder."""

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from npuzzle.i18n import DEFAULT_LANGUAGE, STRINGS


def default_settings_path() -> Path:
    base = os.environ.get("APPDATA") or os.environ.get("XDG_CONFIG_HOME")
    root = Path(base) if base else Path.home() / ".config"
    return root / "npuzzle" / "settings.json"


@dataclass
class Settings:
    language: str = DEFAULT_LANGUAGE

    @classmethod
    def load(cls, path: Path | None = None) -> "Settings":
        """Read the settings, falling back to defaults if the file is missing or damaged."""
        try:
            data = json.loads((path or default_settings_path()).read_text(encoding="utf-8"))
            language = data["language"]
        except (OSError, ValueError, KeyError, TypeError):
            return cls()
        return cls(language if language in STRINGS else DEFAULT_LANGUAGE)

    def save(self, path: Path | None = None) -> None:
        target = path or default_settings_path()
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(asdict(self)), encoding="utf-8")
        except OSError:
            pass  # Losing a preference should never interrupt the game.
