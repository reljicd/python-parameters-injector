from typing import Union, List, Dict

import yaml


def parse_yaml(file: str) -> Union[Dict, List]:
    """Parses .yaml file into corresponding dictionary.

    Args:
        file: - Path to .yaml file.

    Returns:
        Dictionary parsed from .yaml file.
    """

    with open(file, 'r') as f:
        return yaml.load(f)
