# src/segmented_docstring/config.py

import toml
from pathlib import Path
from typing import Dict, Any

from colored_custom_logger import CustomLogger

logger = CustomLogger.get_logger("config")

DEFAULT_CONFIG = {
    'source_folder': 'segmented_src',
    'output_folder': 'src',
    'barecode_extension': '.barecode.py',
    'docstring_extension': '.docstring.py',
    'recursion': True,
    'dry_run': False
}

class ConfigError(Exception):
    """Base exception for configuration-related errors."""
    pass

class ConfigFileNotFoundError(ConfigError):
    """Raised when the configuration file is not found."""
    pass

class ConfigFileParseError(ConfigError):
    """Raised when there's an error parsing the configuration file."""
    pass

def read_config(config_path: Path = None) -> Dict[str, Any]:
    """
    Read configuration from a TOML file or return default values.

    Args:
        config_path (Path, optional): Path to the configuration file. Defaults to None.

    Returns:
        Dict[str, Any]: Configuration dictionary with all settings.

    Raises:
        ConfigFileNotFoundError: If the specified config file is not found.
        ConfigFileParseError: If there's an error parsing the config file.
    """
    if config_path is None:
        config_path = Path.cwd() / '.segmentedrc'

    config = DEFAULT_CONFIG.copy()

    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                file_config = toml.load(f)
            if 'segmented_docstring' in file_config:
                config.update(file_config['segmented_docstring'])
            logger.info("Configuration loaded from %s", config_path)
        except toml.TomlDecodeError as e:
            logger.error("Error parsing configuration file: %s", e)
            raise ConfigFileParseError(f"Error parsing configuration file: {e}") from e
        except IOError as e:
            logger.error("Error reading configuration file: %s", e)
            raise ConfigFileNotFoundError(f"Error reading configuration file: {e}") from e
    else:
        logger.warning("Configuration file not found at %s. Using default configuration.", config_path)

    logger.debug("Final configuration: %s", config)
    return config

__version__ = '0.1.8'
