from datetime import datetime, timezone
import logging
import os
from subprocess import call, DEVNULL, STDOUT
from tempfile import mkdtemp

from .base import BaseInput


class MySQLInput(BaseInput):

    def __init__(
        self,
        name: str,
        host: str,
        port: int,
        username: str,
        password: str,
        database_name: str,
    ):
        super().__init__(name)
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._database_name = database_name
        self._logger = logging.getLogger("automated_backup_utilities")

    def backup(self) -> str:
        name = self.get_name()

        self._logger.info(
            "Backing up MySQL database with name: %s",
            self._database_name,
        )

        output_folder = mkdtemp()
        now = datetime.now(timezone.utc)
        now_str = now.strftime("%Y-%m-%d_%H:%M:%S")

        filename_sql = f"{name}_{now_str}.sql"
        output_path_sql = os.path.join(output_folder, filename_sql)
        filename_tar_gz = f"{name}_{now_str}.tar.gz"
        output_path_tar_gz = os.path.join(output_folder, filename_tar_gz)

        command = f"""
            MYSQL_PWD="{self._password}" mysqldump \
                 -h {self._host} \
                 --port={self._port} \
                 -u {self._username} \
                 {self._database_name} \
                > {output_path_sql}
        """
        call(command, shell=True, stdout=DEVNULL, stderr=STDOUT)

        command = f"""cd {output_folder} \
             && tar zcvf {filename_tar_gz} {filename_sql}
        """

        call(command, shell=True, stdout=DEVNULL, stderr=STDOUT)

        os.remove(output_path_sql)

        self._logger.info(
            "Finished Backing up MySQL database: %s",
            self._database_name,
        )

        return output_path_tar_gz
