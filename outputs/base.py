class BaseOutput:

    def store(self, name: str, file_path: str, content_type: str | None):
        raise NotImplementedError("Not implemented")

    def list_files(self) -> list:
        raise NotImplementedError("Not implemented")

    def remove(self, name: str):
        raise NotImplementedError("Not implemented")
