import pytest
import os

import sky_atc.runpod
from sky_atc.runpod import RunPodProvider

def test_basic():
    assert "RUNPOD_API_KEY" in os.environ

    provider = RunPodProvider("integration-test")

    pods = provider.list_pods()
    assert len(pods) == 0, f"{pods}"

    provider.create_pod("my-node", "ubuntu:latest", "NVIDIA GeForce RTX 3070")

    pods = provider.list_pods()
    assert len(pods) == 1, f"{pods}"

    for pod in pods:
        print("Deleted", pod)
        provider.delete_pod(pod)

    pods = provider.list_pods()
    assert len(pods) == 0, f"{pods}"

