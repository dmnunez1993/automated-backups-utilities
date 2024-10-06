import logging
from minio import Minio

from .base import BaseOutput


class MinioOutput(BaseOutput):

    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        secure: bool,
        bucket_name: str,
    ):
        self._endpoint = endpoint
        self._access_key = access_key
        self._secret_key = secret_key
        self._secure = secure
        self._bucket_name = bucket_name
        self._logger = logging.getLogger("automated_backup_utilities")

    def _get_client(self):
        return Minio(
            self._endpoint,
            access_key=self._access_key,
            secret_key=self._secret_key,
            secure=self._secure,
        )

    def store(
        self,
        name: str,
        file_path: str,
        content_type: str | None = None,
    ):
        self._logger.info(
            "Uploading backup to Minio: %s",
            name,
        )
        self._fput_object(name, file_path, content_type)

        self._logger.info(
            "Finished uploading backup to Minio: %s",
            name,
        )

    def list_files(self) -> list:
        client = self._get_client()

        objs = client.list_objects(self._bucket_name)

        return [obj.object_name for obj in objs]

    def remove(self, name):
        client = self._get_client()
        self._logger.info(
            "Removing object from Minio: %s",
            name,
        )
        client.remove_object(self._bucket_name, name)

        self._logger.info(
            "Finished removing object from Minio: %s",
            name,
        )

    def _fput_object(
        self,
        name: str,
        file_path: str,
        content_type: str | None = None,
    ):
        client = self._get_client()
        client.fput_object(
            self._bucket_name,
            name,
            file_path,
            content_type,
        )
