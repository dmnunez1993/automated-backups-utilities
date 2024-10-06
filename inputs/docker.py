from datetime import datetime, timezone
import logging
import os
from subprocess import call, DEVNULL, STDOUT
from tempfile import mkdtemp

from .base import BaseInput


class DockerInput(BaseInput):

    def __init__(self, name: str, volume_name: str):
        super().__init__(name)
        self._volume_name = volume_name
        self._logger = logging.getLogger("automated_backup_utilities")

    def backup(self) -> str:
        name = self.get_name()

        self._logger.info(
            "Backing up Docker Volume with name: %s",
            self._volume_name,
        )

        output_folder = mkdtemp()
        now = datetime.now(timezone.utc)
        now_str = now.strftime("%Y-%m-%d_%H:%M:%S")

        filename = f"{name}_{now_str}.tar.gz"

        command = f"""
            docker run --rm -v {self._volume_name}:/data -v {output_folder}:/backup \
                busybox tar zcvf /backup/{filename} /data
        """
        call(command, shell=True, stdout=DEVNULL, stderr=STDOUT)
        uid = os.getuid()

        command = f"""
            docker run --rm -v {output_folder}:/backup busybox chown {uid}:{uid} /backup/{filename}
        """
        call(command, shell=True, stdout=DEVNULL, stderr=STDOUT)

        self._logger.info(
            "Finished Backing up Docker Volume: %s",
            self._volume_name,
        )

        return os.path.join(output_folder, filename)
