import sky_atc.generated.pod_provider_pb2 as pod_provider_pb2
import sky_atc.generated.pod_provider_pb2_grpc as pod_provider_pb2_grpc
from sky_atc.k8s_util import json_string_to_node, json_string_to_pod, v1_type_to_dict
from sky_atc.models import Container, ContainerProvider, AlreadyExistsError

import logging
import json
import grpc
from kubernetes import client

logger = logging.getLogger(__name__)

def _make_container_provider_name(pod : client.V1Pod) -> str:
    return f"{pod.metadata.namespace}/{pod.metadata.name}"

class PodProviderServicer(pod_provider_pb2_grpc.PodProviderServicer):

    def __init__(self, container_provider : ContainerProvider):
        self.container_provider = container_provider

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

        name = _make_container_provider_name(pod)

        assert len(pod.spec.containers) == 1, f"Expected a single container in the pod. Got {pod.spec.containers}"
        image = pod.spec.containers[0].image
        hardware = pod.metadata.labels.get("virtual-kubelet.io/hardwareType")

        try:
            self.container_provider.create_container(name, image, hardware)
        except AlreadyExistsError as e:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(str(e))
            raise
        else:
            return pod_provider_pb2.CreatePodReply()

    def PrunePods(self, request, context):
        """Missing associated documentation comment in .proto file."""
        logger.info(f"Got PrunePods request. {request}")
        pods = [json_string_to_pod(pod_json) for pod_json in request.core_v1_pod_jsons_to_keep]

        container_keys = {
            _make_container_provider_name(pod) for pod in pods
        }

        for container in self.container_provider.list_containers():
            if container.name not in container_keys:
                logger.info(f"Deleting {container}.")
                self.container_provider.delete_container(container)

        return pod_provider_pb2.PrunePodsReply()

    def GetPodStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        logger.info(f"Got GetPodStatus request. {request}")
        pod = json_string_to_pod(request.core_v1_pod_json)

        try:
            cloud_container = self._get_container(_make_container_provider_name(pod))
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

    def _get_container(self, name) -> Container:
        containers = self.container_provider.list_containers()
        all_names = []
        for container in containers:
            if container.name == name:
                return container
            all_names.append(container.name)
        raise KeyError(f"Couldn't find a container named {name}. Only found {all_names}")
