import pytest
import os

from sky_atc.modal import ModalProvider

def test_basic():
    provider = ModalProvider("integration-test")

    print("Ensure there's no running pods")
    pods = provider.list_pods()
    assert len(pods) == 0, f"{pods}"

    print("Create a pod")
    print(provider.create_pod("my-node", "pytorch/pytorch:2.1.1-cuda12.1-cudnn8-runtime", "NVIDIA GeForce RTX 3070"))

    print("Make sure there's a running pod now.")
    pods = provider.list_pods()
    assert len(pods) == 1, f"{pods}"

    print("Clean up pods.")
    for pod in pods:
        print("Deleted", pod)
        provider.delete_pod(pod)

    print("Ensure there's no running pods")
    pods = provider.list_pods()
    assert len(pods) == 0, f"{pods}"
