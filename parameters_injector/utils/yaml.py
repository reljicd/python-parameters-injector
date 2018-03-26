from typing import Union, List, Dict

import yaml


def parse_yaml(path_to_yaml: str) -> Union[Dict, List]:
    """Parses .yaml file into corresponding dictionary.

    Args:
        path_to_yaml: - Path to .yaml file.

    Returns:
        Dictionary parsed from .yaml file.
    """

    with open(path_to_yaml, 'r') as f:
        return yaml.load(f)
