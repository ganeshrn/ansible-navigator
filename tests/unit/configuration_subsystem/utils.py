""" utility func used by adjacent tests
"""
import os

from typing import Dict
from typing import List
from typing import NamedTuple

import pytest

from ansible_navigator.configuration_subsystem.configurator import Configurator

from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.configuration_subsystem.definitions import Entry
from ansible_navigator.configuration_subsystem.definitions import Message

from ansible_navigator.configuration_subsystem.navigator_configuration import NavigatorConfiguration

from ansible_navigator.yaml import yaml
from ansible_navigator.yaml import Loader

from ...defaults import FIXTURES_DIR

TEST_FIXTURE_DIR = os.path.join(FIXTURES_DIR, "unit", "configuration_subsystem")


class GenerateConfigResponse(NamedTuple):
    """obj for generate_config_response"""

    messages: List[Message]
    errors: List[str]
    application_configuration: ApplicationConfiguration
    settings_contents: Dict


def _generate_config(params=None, setting_file_name=None) -> GenerateConfigResponse:
    """Generate a configuration given a settings file"""
    if params is None:
        params = []

    if setting_file_name:
        settings_file_path = os.path.join(TEST_FIXTURE_DIR, setting_file_name)
        with open(settings_file_path) as file:
            try:
                settings_contents = yaml.load(file, Loader=Loader)
            except yaml.parser.ParserError:
                # let the config subsystem catch the invalid yaml file
                settings_contents = {}
    else:
        settings_file_path = ""
        settings_contents = {}

    application_configuration = NavigatorConfiguration
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params,
        settings_file_path=settings_file_path or None,
    )
    messages, errors = configurator.configure()
    return GenerateConfigResponse(
        messages=messages,
        errors=errors,
        application_configuration=application_configuration,
        settings_contents=settings_contents,
    )


@pytest.fixture(name="generate_config")
def fixture_generate_config():
    """generate a config"""
    return _generate_config


def id_for_base(val):
    """Return an id for a param set"""
    if val is None:
        return "No base params"
    if "editor-command" in val:
        return "Long base params"
    if "ecmd" in val:
        return "Short base params"
    return "Unknown base params"


def id_for_cli(val):
    """Generate an id for a cli entry"""
    if isinstance(val, str):
        return val
    return ""


def id_for_name(val):
    """Return an id based on entry name"""
    if isinstance(val, Entry):
        return val.name
    return ""


def id_for_settings(val):
    """Generate an id for a settings entry"""
    if val in ["DEFAULT_CFG", "USER_CFG"]:
        return f"others={val}"
    if val == "ansible-navigator_empty.yml":
        return "empty settings file"
    if val == "ansible-navigator.yml":
        return "full settings file"
    return val