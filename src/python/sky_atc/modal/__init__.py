import asyncio
from concurrent.futures import ThreadPoolExecutor
import docker
import modal
from modal.client import _Client
from modal.environments import ensure_env
from modal_proto import api_pb2
import subprocess

from sky_atc import PodProvider, Pod
from typing import Any, List

def _make_rpc(endpoint : str, request : Any, executor):
    async def aio_fn():
        client = await _Client.from_env()
        stub_endpoint = getattr(client._stub, endpoint)
        # Modal does some "retry transient" logic, which sounds like a good
        # idea, maybe we should do that too?
        result = await stub_endpoint(request, timeout=5)
        await client._close()
        return result
    return asyncio.run(aio_fn())


class ModalProvider(PodProvider):

    def __init__(self, namespace : str):
        self.namespace = namespace
        self.docker_client = docker.APIClient()
        self.executor = ThreadPoolExecutor(1)

    def create_pod(self, name : str, image : str, hardware : Any):
        cmd = self._get_image_cmd(image)

        image = modal.Image.from_registry(image)

        stub = modal.Stub(f"{self.namespace}.{name}")
        cmd_runner = stub.function(image=image, concurrency_limit=1)(subprocess.run)

        deploy_result = modal.runner.deploy_stub(stub)
        function_call = cmd_runner.spawn(cmd)

        return deploy_result, function_call

    def list_pods(self):
        request = api_pb2.AppListRequest(environment_name=ensure_env())
        response = _make_rpc("AppList", request, self.executor)

        pods = []
        for app in response.apps:
            if app.state == api_pb2.APP_STATE_DEPLOYED and app.description.startswith(f"{self.namespace}."):
                pods.append(Pod(
                    id=app.app_id,
                    name=app.description,
                    _provider_specific=app
                ))
        return pods

    def delete_pod(self, pod : Pod):
        request = api_pb2.AppStopRequest(app_id=pod.id, source=api_pb2.APP_STOP_SOURCE_PYTHON_CLIENT)
        response = _make_rpc("AppStop", request, self.executor)

    def _get_image_cmd(self, image : str) -> List[str]:
        """TODO: This implementation pulls the image. Ideally do something
        like this https://ops.tips/blog/inspecting-docker-image-without-pull/

        """
        parts = image.split(":")
        # Are ':' allowed in images/tags?
        image, tag = ":".join(parts[:-1]), parts[-1]
        self.docker_client.pull(image, tag)
        image = self.docker_client.inspect_image(f"{image}:{tag}")

        entrypoint = image["Config"].get("Entrypoint") or ["/bin/sh", "-c", "#(nop) "]
        cmd = image["Config"].get("Cmd", [])
        return entrypoint + cmd

