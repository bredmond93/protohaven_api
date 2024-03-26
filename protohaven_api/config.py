"""Loads config.yaml"""
from functools import cache
from os import getenv

import pytz
import yaml

tz = pytz.timezone("US/Eastern")


@cache
def get_config():
    """Fetches the config"""
    with open(getenv("PH_CONFIG", "config.yaml"), "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg
