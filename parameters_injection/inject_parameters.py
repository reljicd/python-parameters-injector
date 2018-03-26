import pathlib
from functools import wraps
from typing import Callable, Dict

from parameters_injection.exceptions.nonexistent_key import NonexistentKeyException
from parameters_injection.exceptions.nonexistent_parameter import NonexistentParameterException
from parameters_injection.exceptions.unsupported_config_file_extension import UnsupportedConfigFileExtensionException
from parameters_injection.utils import json
from parameters_injection.utils import yaml


def inject_parameters(config_file: str,
                      key: str = None,
                      parameters_to_inject: str = None) -> Callable:
    """ Util decorator for injection of parameters from config files

    Args:
        config_file: File path of config file
        key: Top level key in config file, in case the config file is made from several sub configs, each with key
        parameters_to_inject: String of parameters to inject, separated by whitespace

    Returns:
        Parametrized decorator
    """

    config_file_suffix = pathlib.Path(config_file).suffix

    if config_file_suffix == '.yaml':
        config_dict = yaml.parse_yaml(config_file)
    elif config_file_suffix == '.json':
        config_dict = json.parse_json(config_file)
    else:
        raise UnsupportedConfigFileExtensionException

    if parameters_to_inject:
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
    else:
        parameters = {}

    def decorator(func: Callable) -> Callable:

        @wraps(func)
        def func_wrapper(*args, **kwargs):

            # Override parameters from config file wih explicitly passed parameters
            for kwarg_key in kwargs.keys():
                if kwarg_key in parameters:
                    del parameters[kwarg_key]

            return func(*args, **kwargs, **parameters)

        return func_wrapper

    return decorator


def get_sub_dict_for_key_in_dot_notation(dictionary: Dict, key: str) -> Dict:
    if len(key.split('.')) > 1:
        top_key = key.split('.')[0]
        bottom_key = key.replace(top_key + '.', '', 1)
        return get_sub_dict_for_key_in_dot_notation(dictionary=dictionary[top_key], key=bottom_key)
    else:
        return dictionary[key]
