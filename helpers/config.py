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
import copy

# datatypes to validate config against
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

# set format of warnings
warnings.formatwarning = lambda msg, cat, fname, lno, line=None: f"{msg}\n"

def merge_config(dct, merge_dct):
    # recursively merge merge_dct into dct (mutates dct)
    for key, value in merge_dct.items():
        if (key in dct and isinstance(dct[key], dict) and isinstance(merge_dct[key], dict)):
            merge_config(dct[key], merge_dct[key])
        else:
            dct[key] = merge_dct[key]
    return dct

def _validate(config, schema, defaults, prefix=""):
    # in-place validate `config` against `schema`, replace with defaults if type mismatch
    errors = []

    for key, expected in schema.items():
        default_value = defaults.get(key)

        # if user didn't include the key at all, skip (merge already filled defaults)
        if key not in config:
            continue

        value = config[key]

        if isinstance(expected, dict):
            # nesting expected
            if not isinstance(value, dict):
                errors.append(
                    f"Config: {prefix}{key} expected dict, got {type(value).__name__}"
                )
                # replace entire subtree with default subtree (or empty dict if missing)
                config[key] = default_value if isinstance(default_value, dict) else {}
            else:
                nested_defaults = default_value if isinstance(default_value, dict) else {}
                errors.extend(_validate(config[key], expected, nested_defaults, prefix=f"{prefix}{key}."))
        else:
            # primitive expected type
            if not isinstance(value, expected):
                errors.append(
                    f"Config: {prefix}{key} expected {expected.__name__}, got {type(value).__name__}: {value}. Using fallback: {default_value}"
                )
                # replace bad value with the pristine default fallback
                config[key] = default_value

    return errors

def validate_config(config, defaults):
    errors = _validate(config, SCHEMA, defaults)

    for e in errors:
        warnings.warn(f"\033[93m[WARNING]\033[0m {e}")

    return errors

def set_config():
    default_config_path = Path(current_app.root_path) / "helpers" / "defaults.toml"
    user_config_path = Path(current_app.root_path) / "sirenus.toml"

    with open(user_config_path, 'rb') as cfg:
        user_config = tomllib.load(cfg)

    with open(default_config_path, 'rb') as cfg:
        default_config = tomllib.load(cfg)

    # merging a deep copy of defaults so `default_config` stays pristine
    merged_config = merge_config(copy.deepcopy(default_config), user_config)

    # validate using the pristine default_config as the fallback source
    validate_config(merged_config, default_config)

    return merged_config
