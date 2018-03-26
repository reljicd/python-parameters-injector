import pytest

from parameters_injector.exceptions.nonexistent_key import NonexistentKeyException
from parameters_injector.exceptions.nonexistent_parameter import NonexistentParameterException
from parameters_injector.exceptions.unsupported_config_file_extension import UnsupportedConfigFileExtensionException
from parameters_injector.inject_parameters import inject_parameters
from parameters_injector.utils.yaml import parse_yaml

CONFIG_FILE_YAML = 'tests/data/test_inject_parameters.yaml'
CONFIG_FILE_JSON = 'tests/data/test_inject_parameters.json'
CONFIG_FILE_UNSUPPORTED = 'tests/data/test_inject_parameters.unsupported'
CONFIG_DICT = parse_yaml(CONFIG_FILE_YAML)
PARAMETER_1 = 'parameter_1'


def test_inject_all_parameters_yaml():
    inject_all_parameters(config_file=CONFIG_FILE_YAML)


def test_inject_all_parameters_json():
    inject_all_parameters(config_file=CONFIG_FILE_JSON)


def inject_all_parameters(config_file: str):
    @inject_parameters(config_file=config_file, parameters_to_inject='parameter_2, parameter_3, parameter_4')
    def injected_function(parameter_1,
                          parameter_2: str = None,
                          parameter_3: str = None,
                          parameter_4: str = None):
        assert parameter_1 == PARAMETER_1
        assert parameter_2 == CONFIG_DICT['parameter_2']
        assert parameter_3 == CONFIG_DICT['parameter_3']
        assert parameter_4 == CONFIG_DICT['parameter_4']

    injected_function(parameter_1=PARAMETER_1)


def test_inject_some_parameters_yaml():
    inject_some_parameters(config_file=CONFIG_FILE_YAML)


def test_inject_some_parameters_json():
    inject_some_parameters(config_file=CONFIG_FILE_JSON)


def inject_some_parameters(config_file: str):
    @inject_parameters(config_file=config_file, parameters_to_inject='parameter_3, parameter_4')
    def injected_function(parameter_1,
                          parameter_2: str = None,
                          parameter_3: str = None,
                          parameter_4: str = None):
        assert parameter_1 == PARAMETER_1
        assert parameter_2 is None
        assert parameter_3 == CONFIG_DICT['parameter_3']
        assert parameter_4 == CONFIG_DICT['parameter_4']

    injected_function(parameter_1=PARAMETER_1)


def test_override_injected_parameters_yaml():
    override_injected_parameters(config_file=CONFIG_FILE_YAML)


def test_override_injected_parameters_json():
    override_injected_parameters(config_file=CONFIG_FILE_JSON)


def override_injected_parameters(config_file: str):
    overridden_parameter_2 = 'overridden_parameter_2'

    @inject_parameters(config_file=config_file, parameters_to_inject='parameter_3, parameter_4')
    def injected_function(parameter_1,
                          parameter_2: str = None,
                          parameter_3: str = None,
                          parameter_4: str = None):
        assert parameter_1 == PARAMETER_1
        assert parameter_2 == overridden_parameter_2
        assert parameter_3 == CONFIG_DICT['parameter_3']
        assert parameter_4 == CONFIG_DICT['parameter_4']

    injected_function(parameter_1=PARAMETER_1, parameter_2=overridden_parameter_2)


def test_inject_parameters_with_key_yaml():
    inject_parameters_with_key(config_file=CONFIG_FILE_YAML)


def test_inject_parameters_with_key_json():
    inject_parameters_with_key(config_file=CONFIG_FILE_JSON)


def inject_parameters_with_key(config_file: str):
    @inject_parameters(config_file=config_file, key='key', parameters_to_inject='parameter_2, parameter_3, parameter_4')
    def injected_function(parameter_1,
                          parameter_2: str = None,
                          parameter_3: str = None,
                          parameter_4: str = None):
        assert parameter_1 == PARAMETER_1
        assert parameter_2 == CONFIG_DICT['key']['parameter_2']
        assert parameter_3 == CONFIG_DICT['key']['parameter_3']
        assert parameter_4 == CONFIG_DICT['key']['parameter_4']

    injected_function(parameter_1=PARAMETER_1)


def test_inject_parameters_with_zero_parameters_yaml():
    inject_parameters_with_zero_parameters(config_file=CONFIG_FILE_YAML)


def test_inject_parameters_with_zero_parameters_json():
    inject_parameters_with_zero_parameters(config_file=CONFIG_FILE_JSON)


def inject_parameters_with_zero_parameters(config_file: str):
    @inject_parameters(config_file=config_file)
    def injected_function(parameter_1,
                          parameter_2: str = None,
                          parameter_3: str = None,
                          parameter_4: str = None):
        assert parameter_1 == PARAMETER_1
        assert parameter_2 is None
        assert parameter_3 is None
        assert parameter_4 is None

    injected_function(parameter_1=PARAMETER_1)


def test_inject_nonexistent_parameter_yaml():
    inject_nonexistent_parameter(config_file=CONFIG_FILE_YAML)


def test_inject_nonexistent_parameter_json():
    inject_nonexistent_parameter(config_file=CONFIG_FILE_JSON)


def inject_nonexistent_parameter(config_file: str):
    with pytest.raises(NonexistentParameterException):
        @inject_parameters(config_file=config_file, parameters_to_inject='nonexistent_parameter')
        def injected_function():
            pass


def test_unsupported_config_file_extension():
    with pytest.raises(UnsupportedConfigFileExtensionException):
        @inject_parameters(config_file=CONFIG_FILE_UNSUPPORTED)
        def injected_function():
            pass


def test_nonexistent_config_file():
    with pytest.raises(FileNotFoundError):
        @inject_parameters(config_file='nonexistent_file.yaml')
        def injected_function():
            pass


def test_nonexistent_key():
    with pytest.raises(NonexistentKeyException):
        @inject_parameters(config_file=CONFIG_FILE_YAML, key='nonexistent_key', parameters_to_inject='parameter_2')
        def injected_function():
            pass
