from __future__ import annotations

import sys
from pathlib import Path

from msgspec import DecodeError, yaml

from hanya.tooling import setup_logger

from .client import Hanya
from .karma import KarmaConfig


def cli_main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=Path, required=True, help="Path to config file")
    args = parser.parse_args()

    config_path: Path = args.config
    config_path = config_path.resolve(strict=True)

    try:
        decoded_conf = yaml.decode(config_path.read_bytes(), type=KarmaConfig)
    except DecodeError as exc:
        print(f"Invalid config file: {exc}")
        sys.exit(1)

    log_path = Path(decoded_conf.logpath) / decoded_conf.logfile
    logger = setup_logger(log_path)

    logger.info("Starting hanya...")
    hanya = Hanya(decoded_conf)
    try:
        hanya.start()
    except KeyboardInterrupt:
        logger.warning("KeyboardInterrupt detected, stopping...")
        hanya.stop()


if __name__ == "__main__":
    cli_main()
