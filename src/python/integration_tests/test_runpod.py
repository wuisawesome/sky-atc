import pytest
import os
import runpod.api.ctl_commands

import sky_atc.runpod
from sky_atc.runpod import RunPodProvider, AlreadyExistsError

def test_basic():
    assert "RUNPOD_API_KEY" in os.environ

    provider = RunPodProvider("integration-test")

    print("available hardware: ", runpod.api.ctl_commands.get_gpus())

    pods = provider.list_pods()
    assert len(pods) == 0, f"{pods}"

    provider.create_pod("my-node", "ubuntu:latest", "NVIDIA GeForce RTX 3070")

    with pytest.raises(AlreadyExistsError):
        provider.create_pod("my-node", "ubuntu:latest", "NVIDIA GeForce RTX 3070")

    pods = provider.list_pods()
    assert len(pods) == 1, f"{pods}"

    for pod in pods:
        print("Deleted", pod)
        provider.delete_pod(pod)

    pods = provider.list_pods()
    assert len(pods) == 0, f"{pods}"

