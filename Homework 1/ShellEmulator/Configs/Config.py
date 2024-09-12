import json, os

def get_config():
    with open("Configs/config.json") as f:
        return json.load(f)