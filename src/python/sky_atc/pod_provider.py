import sky_atc.generated.pod_provider_pb2 as pod_provider_pb2
import sky_atc.generated.pod_provider_pb2_grpc as pod_provider_pb2_grpc
from sky_atc.k8s_util import json_string_to_node

import logging
import json

logger = logging.getLogger(__name__)


class PodProviderServicer(pod_provider_pb2_grpc.PodProviderServicer):

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

