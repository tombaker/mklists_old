"""@@@"""

import io
import os
from .constants import (
    CONFIG_YAMLFILE_NAME,
    CONFIG_YAMLFILE_YAMLSTR,
    RULE_YAMLFILE_NAME,
    GRULE_YAMLFILE_STARTER_YAMLSTR,
    RULEA_YAMLFILE_STARTER_YAMLSTR,
    RULEB_YAMLFILE_STARTER_YAMLSTR,
)


def initialize_config_yamlfiles():
    """Initialize configuration YAML file"""
    config_path = os.path.join(os.getcwd())
    config_file = os.path.join(config_path, CONFIG_YAMLFILE_NAME)
    grule_file = os.path.join(config_path, RULE_YAMLFILE_NAME)
    os.makedirs(os.path.join(config_path, "a"))
    os.makedirs(os.path.join(config_path, "b"))
    rulea_file = os.path.join(config_path, "a", RULE_YAMLFILE_NAME)
    ruleb_file = os.path.join(config_path, "b", RULE_YAMLFILE_NAME)
    io.open(config_file, "w", encoding="utf-8").write(CONFIG_YAMLFILE_YAMLSTR)
    io.open(grule_file, "w", encoding="utf-8").write(GRULE_YAMLFILE_STARTER_YAMLSTR)
    io.open(rulea_file, "w", encoding="utf-8").write(RULEA_YAMLFILE_STARTER_YAMLSTR)
    io.open(ruleb_file, "w", encoding="utf-8").write(RULEB_YAMLFILE_STARTER_YAMLSTR)
