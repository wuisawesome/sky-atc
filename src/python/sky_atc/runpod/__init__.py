import runpod
import os
from typing import Any, Optional

class RunPodProvider:

    def __init__(self, namespace : str, api_key : Optional[str] = None):
        self.namespace = namespace

        if api_key is None:
            api_key = os.environ["RUNPOD_API_KEY"]

        runpod.api_key = api_key

    def create_pod(self, name : str, image : str, hardware : Any):

        pass

    def list_pods(self):
        pods = []
        for pod_name, value in runpod.get_pods().items():
            if pod_name.startswith(f"{self.namespace}/"):
                pods.append(value)

        return pods

