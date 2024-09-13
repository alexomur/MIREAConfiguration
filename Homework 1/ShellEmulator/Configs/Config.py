import toml

def get_config() -> dict:
    with open("Configs/config.toml") as f:
        return toml.load(f)