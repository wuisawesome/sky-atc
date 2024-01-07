import pytest
import os
import runpod.api.ctl_commands

import sky_atc.runpod
from sky_atc.runpod import RunPodProvider, AlreadyExistsError

def test_basic():
    assert "RUNPOD_API_KEY" in os.environ

    provider = RunPodProvider("integration-test")

    print("available hardware: ", runpod.api.ctl_commands.get_gpus())

    containers = provider.list_containers()
    assert len(containers) == 0, f"{containers}"

    provider.create_container("my-node", "ubuntu:latest", "NVIDIA GeForce RTX 3070")

    with pytest.raises(AlreadyExistsError):
        provider.create_container("my-node", "ubuntu:latest", "NVIDIA GeForce RTX 3070")

    containers = provider.list_containers()
    print(containers)
    assert len(containers) == 1, f"{containers}"

    for container in containers:
        print("Deleted", container)
        provider.delete_container(container)

    containers = provider.list_containers()
    assert len(containers) == 0, f"{containers}"

