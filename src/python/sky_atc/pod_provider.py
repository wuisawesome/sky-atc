import sky_atc.generated.pod_provider_pb2 as pod_provider_pb2
import sky_atc.generated.pod_provider_pb2_grpc as pod_provider_pb2_grpc
from sky_atc.k8s_util import json_string_to_node, json_string_to_pod

import logging
import json
from abc import ABC
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Pod:
    name : str
    id : str
    _provider_specific : Any


class PodProvider(ABC):
    def create_pod(self, name : str, image : str, hardware : Any):
        raise NotImplemented

    def list_pods(self):
        raise NotImplemented

    def delete_pod(self, pod : Pod):
        raise NotImplemented


class PodProviderServicer(pod_provider_pb2_grpc.PodProviderServicer):

    def __init__(self, pod_provider : PodProvider):
        self.pod_provider = pod_provider

    def ConfigureNode(self, request, context):
        """Missing associated documentation comment in .proto file."""

        logger.info(f"Got ConfigureNode request.")

        node = json_string_to_node(request.core_v1_node_json)

        # These values should be approximately inifinite while being the right
        # width types.
        node_resources = {
            "CPU": 2**30,
            "memory": "100Ti",
            "pods": 2**30
        }

        node.status.capacity = node_resources
        node.status.allocatable = node_resources

        return pod_provider_pb2.ConfigureNodeReply(
            core_v1_node_json = json.dumps(node.to_dict())
        )

    def CreatePod(self, request, context):
        """Missing associated documentation comment in .proto file."""
        logger.info(f"Got CreateNode request. {request}")
        pod = json_string_to_pod(request.core_v1_pod_json)

        name = pod.metadata.name

        assert len(pod.spec.containers) == 1, f"Expected a single container in the pod. Got {pod.spec.containers}"
        image = pod.spec.containers[0].image

        self.pod_provider.create_pod(name, image, "NVIDIA GeForce RTX 3070")

        return pod_provider_pb2.CreatePodReply()

    def DeletePod(self, request, context):
        """Missing associated documentation comment in .proto file."""
        logger.info(f"Got DeleteNode request. {request}")
        kpod = json_string_to_pod(request.core_v1_pod_json)
        name = kpod.metadata.name

        pod = self._get_pod(name)
        self.pod_provider.delete_pod(pod)

        return pod_provider_pb2.DeletePodReply()

    def _get_pod(self, name) -> Pod:
        pods = self.pod_provider.list_pods()
        all_names = []
        for pod in pods:
            if pod.name == name:
                return pod
            all_names.append(pod.name)
        raise KeyError(f"Couldn't find a pod named {name}. Only found {all_names}")
