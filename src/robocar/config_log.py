# log.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import toml


# Function to set up the global logging configuration
def setup_logging():
    root_dir = Path(__file__).parent.parent.parent
    config_path = root_dir / "config.toml"
    config = toml.load(config_path)

    log_file_path = root_dir / config["logging"]["file"]
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, config["logging"]["level"]),
        format=config["logging"]["format"],
    )

    handler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=config["logging"]["max_size"] * 1024 * 1024,
        backupCount=config["logging"]["backup_count"],
    )
    handler.setFormatter(logging.Formatter(config["logging"]["format"]))

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)


# Call the setup function to configure logging when the module is imported
setup_logging()
