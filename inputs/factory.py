from typing import Dict, Any

from .docker import DockerInput
from .mysql import MySQLInput
from .postgresql import PostgreSQLInput
from .types import (
    DOCKER_INPUT_TYPE,
    POSTGRESQL_INPUT_TYPE,
    MYSQL_INPUT_TYPE,
)


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

    if input_type == MYSQL_INPUT_TYPE:
        return MySQLInput(
            name=config["name"],
            host=config["mysql"]["host"],
            port=config["mysql"]["port"],
            username=config["mysql"]["username"],
            password=config["mysql"]["password"],
            database_name=config["mysql"]["database_name"],
        )

    raise NotImplementedError(f"Input of type '{input_type}' not implemented")
