from flask import current_app
from markupsafe import Markup
from pathlib import Path

_svg_cache = {}

def svg(name):
    debug = current_app.debug

    if not debug and name in _svg_cache:
        return _svg_cache[name]

    svg_path = Path(current_app.root_path) / "templates" / "svg" / f"{name}.svg"


    if not svg_path.exists():
        raise FileNotFoundError(f"SVG '{name}' not found at {svg_path}")

    with open(svg_path, encoding="utf-8") as file:
        content = file.read().strip()

    markup = Markup(content)

    if not debug:
        _svg_cache[name] = markup

    return markup
