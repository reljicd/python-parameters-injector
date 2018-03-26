import json
from typing import Union, List, Dict


def parse_json(path_to_json: str) -> Union[Dict, List]:
    """Parses .json file into corresponding dictionary.

    Args:
        path_to_json: - Path to .json file.

    Returns:
        Dictionary parsed from .json file.
    """

    with open(path_to_json, 'r') as f:
        return json.load(f)
