import toml, os

def get_config():
    with open("Configs/config.toml") as f:
        return toml.load(f)