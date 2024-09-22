class BackupHandler:

    def __init__(self, name: str, output_folder: str):
        self._name = name
        self._output_folder = output_folder

    def get_name(self) -> str:
        return self._name

    def get_output_folder(self) -> str:
        return self._output_folder

    def backup(self) -> str:
        raise NotImplementedError("Not implemented")
