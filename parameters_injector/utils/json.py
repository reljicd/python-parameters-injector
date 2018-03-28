import json
from typing import Union, List, Dict


def parse_json(file: str) -> Union[Dict, List]:
    """Parses .json file into corresponding dictionary.

    Args:
        file: - Path to .json file.

    Returns:
        Dictionary parsed from .json file.
    """

    with open(file, 'r') as f:
        return json.load(f)
