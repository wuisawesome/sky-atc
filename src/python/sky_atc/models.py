from abc import ABC
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Container:
    name : str
    id : str
    _provider_specific : Any


class ContainerProvider(ABC):
    def create_container(self, name : str, image : str, hardware : Any):
        raise NotImplemented

    def list_containers(self):
        raise NotImplemented

    def delete_container(self, container : Container):
        raise NotImplemented


class AlreadyExistsError(KeyError):
    pass

