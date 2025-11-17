"""
This helper script allows us to yadda yadda
"""
import tomllib
from flask import current_app
from pathlib import Path



def load_config():
        
    default_config_path = Path(current_app.root_path) / "helpers" / "defaults.toml"
    user_config_path = Path(current_app.root_path) / "sirenus.toml"

    with open(default_config_path, mode="rb") as dcfg:
        default_config = tomllib.load(dcfg)
    
    with open(user_config_path, mode="rb") as ucfg:
        user_config = tomllib.load(ucfg)

    return default_config, user_config

def deep_merge(default_config, user_config):
    final_config = default_config.copy()
    for key, value in user_config.items():
        if isinstance(value, dict) and key in final_config and isinstance(final_config[key], dict):
            final_config[key] = deep_merge(final_config[key], value)
        else:
            final_config[key] = value

    return final_config
