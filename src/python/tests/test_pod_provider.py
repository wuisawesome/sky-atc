import pytest
from sky_atc import PodProviderServicer
from sky_atc.generated import pod_provider_pb2
from sky_atc.k8s_util import json_string_to_node

@pytest.fixture
def servicer():
    return PodProviderServicer()



def test_configure_node(servicer):
    request = pod_provider_pb2.ConfigureNodeRequest(
        core_v1_node_json="{\"metadata\":{\"name\":\"vkubelet\",\"creationTimestamp\":null,\"labels\":{\"kubernetes.io/hostname\":\"vkubelet\",\"kubernetes.io/role\":\"agent\",\"type\":\"virtual-kubelet\"}},\"spec\":{\"taints\":[{\"key\":\"virtual-kubelet.io/provider\",\"value\":\"grpc\",\"effect\":\"NoSchedule\"}]},\"status\":{\"phase\":\"Pending\",\"conditions\":[{\"type\":\"Ready\",\"status\":\"\",\"lastHeartbeatTime\":null,\"lastTransitionTime\":null},{\"type\":\"DiskPressure\",\"status\":\"\",\"lastHeartbeatTime\":null,\"lastTransitionTime\":null},{\"type\":\"MemoryPressure\",\"status\":\"\",\"lastHeartbeatTime\":null,\"lastTransitionTime\":null},{\"type\":\"PIDPressure\",\"status\":\"\",\"lastHeartbeatTime\":null,\"lastTransitionTime\":null},{\"type\":\"NetworkUnavailable\",\"status\":\"\",\"lastHeartbeatTime\":null,\"lastTransitionTime\":null}],\"daemonEndpoints\":{\"kubeletEndpoint\":{\"Port\":0}},\"nodeInfo\":{\"machineID\":\"\",\"systemUUID\":\"\",\"bootID\":\"\",\"kernelVersion\":\"\",\"osImage\":\"\",\"containerRuntimeVersion\":\"\",\"kubeletVersion\":\"\",\"kubeProxyVersion\":\"\",\"operatingSystem\":\"linux\",\"architecture\":\"arm64\"}}}")

    response = servicer.ConfigureNode(request, None)

    node = json_string_to_node(response.core_v1_node_json)
    assert node.status.capacity is not None
    assert node.status.allocatable is not None

