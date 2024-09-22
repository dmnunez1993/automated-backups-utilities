from datetime import datetime, timezone
from subprocess import call
import os

from .base import BackupHandler


class DockerVolumeBackupHandler(BackupHandler):

    def __init__(self, name: str, output_folder: str, volume_name: str):
        super().__init__(name, output_folder)
        self._volume_name = volume_name

    def backup(self) -> str:
        name = self.get_name()
        output_folder = self.get_output_folder()
        now = datetime.now(timezone.utc)
        now_str = now.strftime("%Y-%m-%d_%H:%M:%S")

        filename = f"{name}_{now_str}.tar.gz"

        command = f"""
            docker run --rm -v {self._volume_name}:/data -v {output_folder}:/backup \
                busybox tar zcvf /backup/{filename} /data
        """
        call(command, shell=True)
        uid = os.getuid()

        command = f"""
            docker run --rm -v {output_folder}:/backup busybox chown {uid}:{uid} /backup/{filename}
        """
        call(command, shell=True)
