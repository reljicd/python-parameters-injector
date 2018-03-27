import pathlib
from functools import wraps
from typing import Callable, Dict, List, KeysView

from parameters_injector.exceptions.nonexistent_key import NonexistentKeyException
from parameters_injector.exceptions.nonexistent_parameter import NonexistentParameterException
from parameters_injector.exceptions.unsupported_config_file_extension import UnsupportedConfigFileExtensionException
from parameters_injector.utils import json
from parameters_injector.utils import yaml


def inject_parameters(config_file: str,
                      parameters_to_inject: str,
                      key: str = None) -> Callable:
    """ Util decorator for injection of parameters from config files

    Args:
        config_file: File path of config file
        parameters_to_inject: String of parameters to inject, separated by whitespace
        key: Top level key in config file, in case the config file is made from several sub configs, each with key

    Returns:
        Parametrized decorator
    """
    parameters = parse_parameters_from_config_file(config_file=config_file,
                                                   parameters_to_inject=parameters_to_inject,
                                                   key=key)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            filtered_parameters = filter_explicitly_passed_parameters(parameters_to_inject=parameters,
                                                                      explicitly_passed_parameters=kwargs.keys())

            return func(*args, **kwargs, **filtered_parameters)

        return func_wrapper

    return decorator


def parse_parameters_from_config_file(config_file: str,
                                      parameters_to_inject: str,
                                      key: str = None) -> Dict:
    config_dict = parse_config_file(config_file=config_file)

    if key:
        try:
            config_dict = get_sub_dict_for_key_in_dot_notation(dictionary=config_dict, key=key)
        except KeyError:
            raise NonexistentKeyException
    try:
        parameters = {parameter: config_dict[parameter]
                      for parameter in parameters_to_inject.split(', ')}
    except KeyError:
        raise NonexistentParameterException

    return parameters


def parse_config_file(config_file: str) -> Dict:
    config_file_suffix = pathlib.Path(config_file).suffix

    if config_file_suffix == '.yaml':
        config_dict = yaml.parse_yaml(config_file)
    elif config_file_suffix == '.json':
        config_dict = json.parse_json(config_file)
    else:
        raise UnsupportedConfigFileExtensionException

    return config_dict


def get_sub_dict_for_key_in_dot_notation(dictionary: Dict, key: str) -> Dict:
    if len(key.split('.')) > 1:
        top_key = key.split('.')[0]
        bottom_key = key.replace(top_key + '.', '', 1)
        return get_sub_dict_for_key_in_dot_notation(dictionary=dictionary[top_key], key=bottom_key)
    else:
        return dictionary[key]


def filter_explicitly_passed_parameters(parameters_to_inject: Dict,
                                        explicitly_passed_parameters: KeysView[str]) -> Dict:
    # Override parameters from config file wih explicitly passed parameters
    for explicitly_passed_parameter in explicitly_passed_parameters:
        if explicitly_passed_parameter in parameters_to_inject:
            del parameters_to_inject[explicitly_passed_parameter]
    return parameters_to_inject
