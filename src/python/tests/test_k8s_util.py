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


def test_json_to_pod():
    json = "{\"metadata\":{\"name\":\"nginx\",\"namespace\":\"default\",\"uid\":\"ab48342c-d1d2-4684-852b-c92cb57e8dbf\",\"resourceVersion\":\"22874\",\"creationTimestamp\":\"2023-11-22T22:19:56Z\",\"annotations\":{\"kubectl.kubernetes.io/last-applied-configuration\":\"{\\\"apiVersion\\\":\\\"v1\\\",\\\"kind\\\":\\\"Pod\\\",\\\"metadata\\\":{\\\"annotations\\\":{},\\\"name\\\":\\\"nginx\\\",\\\"namespace\\\":\\\"default\\\"},\\\"spec\\\":{\\\"containers\\\":[{\\\"image\\\":\\\"nginx\\\",\\\"imagePullPolicy\\\":\\\"Always\\\",\\\"name\\\":\\\"nginx\\\",\\\"ports\\\":[{\\\"containerPort\\\":80,\\\"name\\\":\\\"http\\\",\\\"protocol\\\":\\\"TCP\\\"},{\\\"containerPort\\\":443,\\\"name\\\":\\\"https\\\"}]}],\\\"dnsPolicy\\\":\\\"ClusterFirst\\\",\\\"nodeSelector\\\":{\\\"kubernetes.io/role\\\":\\\"agent\\\",\\\"type\\\":\\\"virtual-kubelet\\\"},\\\"tolerations\\\":[{\\\"effect\\\":\\\"NoSchedule\\\",\\\"key\\\":\\\"virtual-kubelet.io/provider\\\",\\\"operator\\\":\\\"Equal\\\",\\\"value\\\":\\\"grpc\\\"}]}}\\n\"},\"managedFields\":[{\"manager\":\"kubectl-client-side-apply\",\"operation\":\"Update\",\"apiVersion\":\"v1\",\"time\":\"2023-11-22T22:19:56Z\",\"fieldsType\":\"FieldsV1\",\"fieldsV1\":{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kubectl.kubernetes.io/last-applied-configuration\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"nginx\\\"}\":{\".\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:ports\":{\".\":{},\"k:{\\\"containerPort\\\":80,\\\"protocol\\\":\\\"TCP\\\"}\":{\".\":{},\"f:containerPort\":{},\"f:name\":{},\"f:protocol\":{}},\"k:{\\\"containerPort\\\":443,\\\"protocol\\\":\\\"TCP\\\"}\":{\".\":{},\"f:containerPort\":{},\"f:name\":{},\"f:protocol\":{}}},\"f:resources\":{},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:nodeSelector\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:terminationGracePeriodSeconds\":{},\"f:tolerations\":{}}}},{\"manager\":\"virtual-kubelet\",\"operation\":\"Update\",\"apiVersion\":\"v1\",\"time\":\"2023-11-22T22:19:56Z\",\"fieldsType\":\"FieldsV1\",\"fieldsV1\":{\"f:status\":{\"f:message\":{},\"f:reason\":{}}},\"subresource\":\"status\"}]},\"spec\":{\"volumes\":[{\"name\":\"kube-api-access-6c5np\",\"projected\":{\"sources\":[{\"serviceAccountToken\":{\"expirationSeconds\":3607,\"path\":\"token\"}},{\"configMap\":{\"name\":\"kube-root-ca.crt\",\"items\":[{\"key\":\"ca.crt\",\"path\":\"ca.crt\"}]}},{\"downwardAPI\":{\"items\":[{\"path\":\"namespace\",\"fieldRef\":{\"apiVersion\":\"v1\",\"fieldPath\":\"metadata.namespace\"}}]}}],\"defaultMode\":420}}],\"containers\":[{\"name\":\"nginx\",\"image\":\"nginx\",\"ports\":[{\"name\":\"http\",\"containerPort\":80,\"protocol\":\"TCP\"},{\"name\":\"https\",\"containerPort\":443,\"protocol\":\"TCP\"}],\"env\":[{\"name\":\"KUBERNETES_PORT_443_TCP_ADDR\",\"value\":\"10.96.0.1\"},{\"name\":\"KUBERNETES_SERVICE_HOST\",\"value\":\"10.96.0.1\"},{\"name\":\"KUBERNETES_SERVICE_PORT\",\"value\":\"443\"},{\"name\":\"KUBERNETES_SERVICE_PORT_HTTPS\",\"value\":\"443\"},{\"name\":\"KUBERNETES_PORT\",\"value\":\"tcp://10.96.0.1:443\"},{\"name\":\"KUBERNETES_PORT_443_TCP\",\"value\":\"tcp://10.96.0.1:443\"},{\"name\":\"KUBERNETES_PORT_443_TCP_PROTO\",\"value\":\"tcp\"},{\"name\":\"KUBERNETES_PORT_443_TCP_PORT\",\"value\":\"443\"}],\"resources\":{},\"volumeMounts\":[{\"name\":\"kube-api-access-6c5np\",\"readOnly\":true,\"mountPath\":\"/var/run/secrets/kubernetes.io/serviceaccount\"}],\"terminationMessagePath\":\"/dev/termination-log\",\"terminationMessagePolicy\":\"File\",\"imagePullPolicy\":\"Always\"}],\"restartPolicy\":\"Always\",\"terminationGracePeriodSeconds\":30,\"dnsPolicy\":\"ClusterFirst\",\"nodeSelector\":{\"kubernetes.io/role\":\"agent\",\"type\":\"virtual-kubelet\"},\"serviceAccountName\":\"default\",\"serviceAccount\":\"default\",\"nodeName\":\"vkubelet\",\"securityContext\":{},\"schedulerName\":\"default-scheduler\",\"tolerations\":[{\"key\":\"virtual-kubelet.io/provider\",\"operator\":\"Equal\",\"value\":\"grpc\",\"effect\":\"NoSchedule\"},{\"key\":\"node.kubernetes.io/not-ready\",\"operator\":\"Exists\",\"effect\":\"NoExecute\",\"tolerationSeconds\":300},{\"key\":\"node.kubernetes.io/unreachable\",\"operator\":\"Exists\",\"effect\":\"NoExecute\",\"tolerationSeconds\":300}],\"priority\":0,\"enableServiceLinks\":true,\"preemptionPolicy\":\"PreemptLowerPriority\"},\"status\":{\"phase\":\"Pending\",\"conditions\":[{\"type\":\"PodScheduled\",\"status\":\"True\",\"lastProbeTime\":null,\"lastTransitionTime\":\"2023-11-22T22:19:56Z\"}],\"message\":\"rpc error: code = Unknown desc = Exception calling application: data {\'f:metadata\': {\'f:annotations\': {\'.\': {}, \'f:kubectl.kubernetes.io/last-applied-configuration\': {}}}, \'f:spec\': {\'f:containers\': {\'k:{\\\"name\\\":\\\"nginx\\\"}\': {\'.\': {}, \'f:image\': {}, \'f:imagePullPolicy\': {}, \'f:name\': {}, \'f:ports\': {\'.\': {}, \'k:{\\\"containerPort\\\":80,\\\"protocol\\\":\\\"TCP\\\"}\': {\'.\': {}, \'f:containerPort\': {}, \'f:name\': {}, \'f:protocol\': {}}, \'k:{\\\"containerPort\\\":443,\\\"protocol\\\":\\\"TCP\\\"}\': {\'.\': {}, \'f:containerPort\': {}, \'f:name\': {}, \'f:protocol\': {}}}, \'f:resources\': {}, \'f:terminationMessagePath\': {}, \'f:terminationMessagePolicy\': {}}}, \'f:dnsPolicy\': {}, \'f:enableServiceLinks\': {}, \'f:nodeSelector\': {}, \'f:restartPolicy\': {}, \'f:schedulerName\': {}, \'f:securityContext\': {}, \'f:terminationGracePeriodSeconds\': {}, \'f:tolerations\': {}}} should be of type object\",\"reason\":\"ProviderFailed\",\"qosClass\":\"BestEffort\"}}"

    result = k8s_util.json_string_to_pod(json)
    assert isinstance(result, client.V1Pod)


def test_pod_status_to_json():
    pod_status = client.V1PodStatus(
        container_statuses= [
            client.V1ContainerStatus(
                name="hello",
                container_id="hello",
                image="my_image",
                image_id="my_image",
                restart_count = 0,
                ready = True,
                started = True,
                state = client.V1ContainerState(
                    running = client.V1ContainerStateRunning(),
                ),
            )
        ]
    )

    as_dict = k8s_util.v1_type_to_dict(pod_status)

    assert as_dict == {
        'containerStatuses': [
            {
                'containerID': 'hello',
                'image': 'my_image',
                'imageID': 'my_image',
                'name': 'hello',
                'ready': True,
                'restartCount': 0,
                'started': True,
                'state': {
                    'running': {},
                }
            }
        ],
    }


