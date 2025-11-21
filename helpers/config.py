"""
This helper script let's us merge the user provided config with the default
values. This makes configuration easier for the user as they can simply
change what they want to change without filling out the entire config

heavily 'inspired' by https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
wink wink
"""
import tomllib
from flask import current_app
from pathlib import Path

def merge_config(dct, merge_dct):
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], dict)): 
            merge_config(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]
    return dct

def validate_config(config):
    match config:
        case {
            "ui": {
                "title": str(),
                "heading": str(),
                "desc": str()
            },
            "app": {
                "sound_dir": str(),
                "sample_rate": int()
            },
        }:
            pass
        case _:
            raise ValueError(f"invalid configuration: {config}")
            

def set_config():
    default_config_path = Path(current_app.root_path) / "helpers" / "defaults.toml"
    user_config_path = Path(current_app.root_path) / "sirenus.toml"

    with open(user_config_path, 'rb') as cfg:
        user_config = tomllib.load(cfg)

    with open(default_config_path, 'rb') as cfg:
        default_config = tomllib.load(cfg)

    config = merge_config(default_config, user_config)
    return config
