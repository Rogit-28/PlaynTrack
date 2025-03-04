from __future__ import annotations

from pathlib import Path

from src.core.config import load_config
from src.utils.logger import setup_logger


logger = setup_logger()


def main() -> None:
    config_path = Path("config.yaml") if Path("config.yaml").exists() else None
    config = load_config(config_path)
    logger.info("PlaynTrack initialized")
    logger.info("Config loaded: %s", config)


if __name__ == "__main__":
    main()
