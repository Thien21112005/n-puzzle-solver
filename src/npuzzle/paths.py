"""Locate bundled files independently of the current working directory."""

from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent / "assets"


def asset_path(*parts: str) -> Path:
    return ASSETS_DIR.joinpath(*parts)
