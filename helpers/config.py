"""
This helper script let's us merge the user provided config with the default
values. This makes configuration easier for the user as they can simply
change what they want to change without filling out the entire config

heavily 'inspired' by https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
wink wink
"""
import tomllib
import warnings
from flask import current_app
from pathlib import Path

# Defining structure
SCHEMA = {
    "ui": {
        "desc": str,
        "heading": str,
        "title": str
    },
    "app": {
        "host": str,
        "port": int,
        "sample_rate": int,
        "sound_dir": str
    },
}

# Clean up warning output vomit
warnings.formatwarning = lambda msg, cat, fname, lno, line=None: f"{msg}\n"

# Function that recursively merges user and default conf
def merge_config(dct, merge_dct):
    for key, value in merge_dct.items():
        if (key in dct and isinstance(dct[key], dict) and isinstance(merge_dct[key], dict)): 
            merge_config(dct[key], merge_dct[key])
        else:
            dct[key] = merge_dct[key]
    return dct

# Internal validation func
def _validate(config, schema, defaults, prefix=""):
    errors = []

    for key, expected in schema.items():
        default_value = defaults[key]

        if key not in config:
            continue

        value = config[key]

        if isinstance(expected, dict):
            if not isinstance(value, dict):
                errors.append(
                    f"Config: {prefix}{key} expected dict, got {type(value).__name__}"
                )
            else:
                errors.extend(_validate(value, expected, defaults.get(key, {}), prefix=f"{prefix}{key}."))
        else:
            # Check types
            if not isinstance(value, expected):
                errors.append(
                    f"Config: {prefix}{key} expected {expected.__name__}, got {type(value).__name__}: {value}"
                )
                config.update({key: default_value})
    return errors

def validate_config(config, defaults):
    errors = _validate(config, SCHEMA, defaults)

    for e in errors:
        warnings.warn(f"\033[93m[WARNING]\033[0m {e}")

    return errors

# Neatly wrap all functions into one main function
def set_config():
    default_config_path = Path(current_app.root_path) / "helpers" / "defaults.toml"
    user_config_path = Path(current_app.root_path) / "sirenus.toml"

    with open(user_config_path, 'rb') as cfg:
        user_config = tomllib.load(cfg)

    with open(default_config_path, 'rb') as cfg:
        default_config = tomllib.load(cfg)

    config = merge_config(default_config, user_config)

    validate_config(config, default_config)

    return config
