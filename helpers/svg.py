"""
This helper script allows us to insert inline SVG's as variables in our
templates. This makes our templates more readable and makes SVG's easier
to work with.
"""
from flask import current_app
from markupsafe import Markup
from pathlib import Path

# Init svg cache for prod
_svg_cache = {}

def svg(name):
    
    # Check if app is running in debug mode
    debug = current_app.debug

    # Return cached svg if present cache in prod
    if not debug and name in _svg_cache:
        return _svg_cache[name]

    # Check if requested svg is present
    svg_path = Path(current_app.root_path) / "templates" / "svg" / f"{name}.svg"

    # Error if not present in path
    if not svg_path.exists():
        raise FileNotFoundError(f"SVG '{name}' not found at {svg_path}")

    # Open and format to print
    with open(svg_path, encoding="utf-8") as file:
        content = file.read().strip()

    markup = Markup(content)

    if not debug:
        _svg_cache[name] = markup

    return markup
