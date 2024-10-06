from typing import Dict, Any, List

import logging
import os

from inputs.base import BaseInput
from inputs.factory import input_factory
from outputs.base import BaseOutput
from outputs.factory import output_factory


class BackupHandler:

    def __init__(
        self,
        name: str,
        max_backups_stored: int,
        data_input: BaseInput,
        data_outputs: List[BaseOutput],
    ):
        self._name = name
        self._max_backups_stored = max_backups_stored
        self._data_input = data_input
        self._data_outputs = data_outputs
        self._logger = logging.getLogger("automated_backup_utilities")

    def backup(self):
        backup_path = self._data_input.backup()

        parts = backup_path.split("/")

        for data_output in self._data_outputs:
            data_output.store(parts[-1], backup_path)

        os.remove(backup_path)

    def clean_previous_backups(self):
        for data_output in self._data_outputs:
            all_backup_files = data_output.list_files()

            backup_files = [
                backup_file for backup_file in all_backup_files
                if backup_file.startswith(self._name)
            ]

            backup_files.sort(reverse=True)

            for idx, backup_file in enumerate(backup_files):
                if idx + 1 > self._max_backups_stored:
                    data_output.remove(backup_file)

    @staticmethod
    def from_config(config: Dict[str, Any]):
        name = config["name"]
        max_backups_stored = config["max_backups_stored"]
        data_input = input_factory(config)
        data_outputs = []
        for output_config in config["outputs"]:
            output = output_factory(output_config)
            data_outputs.append(output)

        return BackupHandler(
            name,
            max_backups_stored,
            data_input,
            data_outputs,
        )
