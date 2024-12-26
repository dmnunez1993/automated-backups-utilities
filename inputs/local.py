from datetime import datetime, timezone
import logging
import os
from subprocess import call, DEVNULL, STDOUT
from tempfile import mkdtemp

from .base import BaseInput


class LocalInput(BaseInput):

    def __init__(self, name: str, path: str):
        super().__init__(name)
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
        filename_tar_gz = f"{name}_{now_str}.tar.gz"
        output_path_tar_gz = os.path.join(output_folder, filename_tar_gz)

        command = f"""cd {self._path} \
             && tar zcvf {output_path_tar_gz} .
        """

        call(command, shell=True, stdout=DEVNULL, stderr=STDOUT)

        return output_path_tar_gz
