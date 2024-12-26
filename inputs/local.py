from datetime import datetime, timezone
import logging
import os
from subprocess import call, DEVNULL, STDOUT
from tempfile import mkdtemp

from .base import BaseInput


class LocalInput(BaseInput):

    def __init__(self, name: str, path: str):
        self._name = name
        self._path = path
        self._logger = logging.getLogger("automated_backup_utilities")

    def backup(self) -> str:
        name = self.get_name()

        self._logger.info(
            "Backing up Local Path: %s",
            self._path,
        )

        output_folder = mkdtemp()
        now = datetime.now(timezone.utc)
        now_str = now.strftime("%Y-%m-%d_%H:%M:%S")
