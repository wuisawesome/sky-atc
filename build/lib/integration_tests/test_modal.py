import pytest
import os

from sky_atc.modal import ModalProvider

def test_basic():
    provider = ModalProvider("integration-test")

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

