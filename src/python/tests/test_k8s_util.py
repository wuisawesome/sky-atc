import pytest
import sky_atc.k8s_util as k8s_util
from kubernetes import client


def test_json_to_node():
    json = "{\"metadata\":{\"name\":\"vkubelet\",\"creationTimestamp\":null,\"labels\":{\"kubernetes.io/hostname\":\"vkubelet\",\"kubernetes.io/role\":\"agent\",\"type\":\"virtual-kubelet\"}},\"spec\":{\"taints\":[{\"key\":\"virtual-kubelet.io/provider\",\"value\":\"grpc\",\"effect\":\"NoSchedule\"}]},\"status\":{\"phase\":\"Pending\",\"conditions\":[{\"type\":\"Ready\",\"status\":\"\",\"lastHeartbeatTime\":null,\"lastTransitionTime\":null},{\"type\":\"DiskPressure\",\"status\":\"\",\"lastHeartbeatTime\":null,\"lastTransitionTime\":null},{\"type\":\"MemoryPressure\",\"status\":\"\",\"lastHeartbeatTime\":null,\"lastTransitionTime\":null},{\"type\":\"PIDPressure\",\"status\":\"\",\"lastHeartbeatTime\":null,\"lastTransitionTime\":null},{\"type\":\"NetworkUnavailable\",\"status\":\"\",\"lastHeartbeatTime\":null,\"lastTransitionTime\":null}],\"daemonEndpoints\":{\"kubeletEndpoint\":{\"Port\":0}},\"nodeInfo\":{\"machineID\":\"\",\"systemUUID\":\"\",\"bootID\":\"\",\"kernelVersion\":\"\",\"osImage\":\"\",\"containerRuntimeVersion\":\"\",\"kubeletVersion\":\"\",\"kubeProxyVersion\":\"\",\"operatingSystem\":\"linux\",\"architecture\":\"arm64\"}}}"

    result = k8s_util.json_string_to_node(json)
    assert isinstance(result, client.V1Node)
    spec = result.spec
    print(spec, type(spec))
    assert isinstance(spec, client.V1NodeSpec)


def test_temp():
    d = {"address": "abc", "type":"xyz"}

    result = k8s_util._construct_v1_type("V1NodeAddress", d)

    assert isinstance(result, client.V1NodeAddress)
