import runpod
import runpod.api.ctl_commands
import os
from typing import Any, Optional, Tuple
import logging

from sky_atc import AlreadyExistsError, ContainerProvider, Container

logger = logging.getLogger(__name__)

class RunPodProvider(ContainerProvider):

    def __init__(self, namespace : str, api_key : Optional[str] = None):
        self.namespace = namespace

        if api_key is None:
            api_key = os.environ["RUNPOD_API_KEY"]

        runpod.api_key = api_key

    def create_container(self, name : str, image : str, hardware : Any):
        runpod_name = f"{self.namespace}/{name}"

        if isinstance(hardware, str):
            # k8s node selector value can't include spaces.
            hardware = hardware.replace("_", " ").strip()
            logger.debug(f"Normalizing hardware name to {hardware}.")

        for pod in self.list_containers():
            if pod._provider_specific["name"] == runpod_name:
                raise AlreadyExistsError(f"A pod already exists with details: {pod}.")

        return runpod.api.ctl_commands.create_pod(runpod_name, image, hardware)

    def list_containers(self):
        pods = []
        namespace_prefix = f"{self.namespace}/"
        for value in runpod.api.ctl_commands.get_pods():
            if value["name"].startswith(namespace_prefix):
                pod = Container(
                    id=value["id"],
                    name=value["name"][len(namespace_prefix):],
                    _provider_specific = value,
                )
                pods.append(pod)

        return pods

    def delete_container(self, container : Container):
        runpod.api.ctl_commands.terminate_pod(container.id)

