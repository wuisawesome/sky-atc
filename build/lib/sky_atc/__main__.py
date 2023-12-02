from sky_atc import PodProviderServicer
from sky_atc.generated import pod_provider_pb2_grpc

from concurrent import futures
import grpc
import logging
import sys

logger = logging.getLogger(__name__)


def configure_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


configure_logging()
logger.info("In python!")

port = "50051"
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

pod_provider_pb2_grpc.add_PodProviderServicer_to_server(PodProviderServicer(), server)

server.add_insecure_port("[::]:" + port)
logger.info("Starting server...")
server.start()
logger.info("Server started, listening on " + port)
server.wait_for_termination()


