from typing import Dict, Any

from .minio import MinioOutput
from .types import MINIO_OUTPUT_TYPE


def output_factory(config: Dict[str, Any]):
    output_type = config["type"]
    if output_type == MINIO_OUTPUT_TYPE:
        return MinioOutput(
            endpoint=config["minio"]["endpoint"],
            access_key=config["minio"]["access_key"],
            secret_key=config["minio"]["secret_key"],
            secure=config["minio"]["secure"],
            bucket_name=config["minio"]["bucket_name"],
        )

    raise NotImplementedError(f"Output of type '{output_type}' not implemented")
