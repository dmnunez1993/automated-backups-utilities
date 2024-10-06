from typing import Dict, Any

from .docker import DockerInput
from .postgresql import PostgreSQLInput
from .types import DOCKER_INPUT_TYPE, POSTGRESQL_INPUT_TYPE


def input_factory(config: Dict[str, Any]):
    input_type = config["type"]
    if input_type == DOCKER_INPUT_TYPE:
        return DockerInput(
            name=config["name"],
            volume_name=config["docker"]["volume_name"],
        )

    if input_type == POSTGRESQL_INPUT_TYPE:
        return PostgreSQLInput(
            name=config["name"],
            host=config["postgresql"]["host"],
            port=config["postgresql"]["port"],
            username=config["postgresql"]["username"],
            password=config["postgresql"]["password"],
            database_name=config["postgresql"]["database_name"],
        )

    raise NotImplementedError(f"Input of type '{input_type}' not implemented")
