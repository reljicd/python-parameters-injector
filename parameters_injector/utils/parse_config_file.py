import pathlib
from typing import Dict

from parameters_injector.exceptions.unsupported_config_file_extension import UnsupportedConfigFileExtensionException
from parameters_injector.utils import json
from parameters_injector.utils import yaml


def parse_config_file(config_file: str) -> Dict:
    config_file_suffix = pathlib.Path(config_file).suffix

    if config_file_suffix == '.yaml':
        config_dict = yaml.parse_yaml(config_file)
    elif config_file_suffix == '.json':
        config_dict = json.parse_json(config_file)
    else:
        raise UnsupportedConfigFileExtensionException

    return config_dict
