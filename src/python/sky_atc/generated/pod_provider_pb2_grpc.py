# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import sky_atc.generated.pod_provider_pb2 as pod__provider__pb2


class PodProviderStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ConfigureNode = channel.unary_unary(
                '/PodProvider/ConfigureNode',
                request_serializer=pod__provider__pb2.ConfigureNodeRequest.SerializeToString,
                response_deserializer=pod__provider__pb2.ConfigureNodeReply.FromString,
                )
        self.CreatePod = channel.unary_unary(
                '/PodProvider/CreatePod',
                request_serializer=pod__provider__pb2.CreatePodRequest.SerializeToString,
                response_deserializer=pod__provider__pb2.CreatePodReply.FromString,
                )
        self.PrunePods = channel.unary_unary(
                '/PodProvider/PrunePods',
                request_serializer=pod__provider__pb2.PrunePodsRequest.SerializeToString,
                response_deserializer=pod__provider__pb2.PrunePodsReply.FromString,
                )
        self.GetPodStatus = channel.unary_unary(
                '/PodProvider/GetPodStatus',
                request_serializer=pod__provider__pb2.GetPodStatusRequest.SerializeToString,
                response_deserializer=pod__provider__pb2.GetPodStatusReply.FromString,
                )


class PodProviderServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ConfigureNode(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreatePod(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PrunePods(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPodStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PodProviderServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ConfigureNode': grpc.unary_unary_rpc_method_handler(
                    servicer.ConfigureNode,
                    request_deserializer=pod__provider__pb2.ConfigureNodeRequest.FromString,
                    response_serializer=pod__provider__pb2.ConfigureNodeReply.SerializeToString,
            ),
            'CreatePod': grpc.unary_unary_rpc_method_handler(
                    servicer.CreatePod,
                    request_deserializer=pod__provider__pb2.CreatePodRequest.FromString,
                    response_serializer=pod__provider__pb2.CreatePodReply.SerializeToString,
            ),
            'PrunePods': grpc.unary_unary_rpc_method_handler(
                    servicer.PrunePods,
                    request_deserializer=pod__provider__pb2.PrunePodsRequest.FromString,
                    response_serializer=pod__provider__pb2.PrunePodsReply.SerializeToString,
            ),
            'GetPodStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPodStatus,
                    request_deserializer=pod__provider__pb2.GetPodStatusRequest.FromString,
                    response_serializer=pod__provider__pb2.GetPodStatusReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'PodProvider', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PodProvider(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ConfigureNode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PodProvider/ConfigureNode',
            pod__provider__pb2.ConfigureNodeRequest.SerializeToString,
            pod__provider__pb2.ConfigureNodeReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreatePod(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PodProvider/CreatePod',
            pod__provider__pb2.CreatePodRequest.SerializeToString,
            pod__provider__pb2.CreatePodReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PrunePods(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PodProvider/PrunePods',
            pod__provider__pb2.PrunePodsRequest.SerializeToString,
            pod__provider__pb2.PrunePodsReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPodStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PodProvider/GetPodStatus',
            pod__provider__pb2.GetPodStatusRequest.SerializeToString,
            pod__provider__pb2.GetPodStatusReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
