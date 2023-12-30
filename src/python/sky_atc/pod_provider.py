import sky_atc.generated.pod_provider_pb2 as pod_provider_pb2
import sky_atc.generated.pod_provider_pb2_grpc as pod_provider_pb2_grpc
from sky_atc.k8s_util import json_string_to_node, json_string_to_pod, v1_type_to_dict

import logging
import json
from abc import ABC
from dataclasses import dataclass
import grpc
from kubernetes import client
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


class AlreadyExistsError(KeyError):
    pass


def _make_pod_provider_name(pod : client.V1Pod) -> str:
    return f"{pod.metadata.namespace}/{pod.metadata.name}"

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

        name = _make_pod_provider_name(pod)

        assert len(pod.spec.containers) == 1, f"Expected a single container in the pod. Got {pod.spec.containers}"
        image = pod.spec.containers[0].image

        try:
            self.pod_provider.create_pod(name, image, "NVIDIA GeForce RTX 3070")
        except AlreadyExistsError as e:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(str(e))
            raise
        else:
            return pod_provider_pb2.CreatePodReply()

    def DeletePod(self, request, context):
        """Missing associated documentation comment in .proto file."""
        logger.info(f"Got DeleteNode request. {request}")
        kpod = json_string_to_pod(request.core_v1_pod_json)
        name = kpod.metadata.name

        pod = self._get_pod(name)
        self.pod_provider.delete_pod(pod)

        return pod_provider_pb2.DeletePodReply()

    def PrunePods(self, request, context):
        """Missing associated documentation comment in .proto file."""
        logger.info(f"Got PrunePods request. {request}")
        pods = [json_string_to_pod(pod_json) for pod_json in request.core_v1_pod_jsons_to_keep]

        container_keys = {
            _make_pod_provider_name(pod) for pod in pods
        }

        for container in self.pod_provider.list_pods():
            if container.name not in container_keys:
                logger.info(f"Deleting {container}.")
                self.pod_provider.delete_pod(container)

        return pod_provider_pb2.PrunePodsReply()

    def GetPodStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        logger.info(f"Got GetPodStatus request. {request}")
        pod = json_string_to_pod(request.core_v1_pod_json)

        try:
            cloud_container = self._get_pod(_make_pod_provider_name(pod))
        except KeyError as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(str(e))
            raise

        assert len(pod.spec.containers) == 1, f"Expected a single container in the pod. Got {pod.spec.containers}"

        k8s_container = pod.spec.containers[0]

        container_status = client.V1ContainerStatus(
            # TODO: Is there ever a case where using the spec information is wrong and `UpdatePod` won't be called?
            image = k8s_container.image,
            name = k8s_container.name,
            # May need to change if we every support restarting?
            restart_count = 0,
            # Our compute providers don't always give us granular enough information to do better than this.
            image_id = k8s_container.image,
            ready = True,
            started = True,
            state = client.V1ContainerState(
                running = client.V1ContainerStateRunning(),
            ),
        )

        pod.status.container_statuses = [container_status]

        # Our compute providers don't always give us granular enough information to do better than this.
        pod.status.phase = "Running"

        status = v1_type_to_dict(pod.status)

        logger.info(f"Returning status {status}")

        return pod_provider_pb2.GetPodStatusReply(
            core_v1_pod_status_json = json.dumps(status),
        )

    def _get_pod(self, name) -> Pod:
        pods = self.pod_provider.list_pods()
        all_names = []
        for pod in pods:
            if pod.name == name:
                return pod
            all_names.append(pod.name)
        raise KeyError(f"Couldn't find a pod named {name}. Only found {all_names}")
