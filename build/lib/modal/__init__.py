import docker

from sky_atc import PodProvider, Pod
from typing import Any

class ModalProvider(PodProvider):

    def __init__(self, namespace : str):
        self.namespace = namespace
        self.docker_client = docker.from_env()

    def create_pod(self, name : str, image : str, hardware : Any):
        return self.docker_client.get(image)

    def list_pods(self):
        return []
        pass

    def delete_pod(self, pod : Pod):
        pass
