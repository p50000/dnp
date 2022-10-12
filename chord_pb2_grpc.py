# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import chord_pb2 as chord__pb2


class RegistryStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.service_info = channel.unary_unary(
                '/Registry/service_info',
                request_serializer=chord__pb2.TEmpty.SerializeToString,
                response_deserializer=chord__pb2.TSuccessResponse.FromString,
                )
        self.register = channel.unary_unary(
                '/Registry/register',
                request_serializer=chord__pb2.TRegisterRequest.SerializeToString,
                response_deserializer=chord__pb2.TRegisterResponse.FromString,
                )
        self.deregister = channel.unary_unary(
                '/Registry/deregister',
                request_serializer=chord__pb2.TDeregisterRequest.SerializeToString,
                response_deserializer=chord__pb2.TSuccessResponse.FromString,
                )
        self.populate_finger_table = channel.unary_unary(
                '/Registry/populate_finger_table',
                request_serializer=chord__pb2.TPopulateFingerTableRequest.SerializeToString,
                response_deserializer=chord__pb2.TPopulateFingerTableResponse.FromString,
                )
        self.get_chord_info = channel.unary_unary(
                '/Registry/get_chord_info',
                request_serializer=chord__pb2.TGetChordInfoRequest.SerializeToString,
                response_deserializer=chord__pb2.TGetChordInfoResponse.FromString,
                )


class RegistryServicer(object):
    """Missing associated documentation comment in .proto file."""

    def service_info(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def register(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deregister(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def populate_finger_table(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_chord_info(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RegistryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'service_info': grpc.unary_unary_rpc_method_handler(
                    servicer.service_info,
                    request_deserializer=chord__pb2.TEmpty.FromString,
                    response_serializer=chord__pb2.TSuccessResponse.SerializeToString,
            ),
            'register': grpc.unary_unary_rpc_method_handler(
                    servicer.register,
                    request_deserializer=chord__pb2.TRegisterRequest.FromString,
                    response_serializer=chord__pb2.TRegisterResponse.SerializeToString,
            ),
            'deregister': grpc.unary_unary_rpc_method_handler(
                    servicer.deregister,
                    request_deserializer=chord__pb2.TDeregisterRequest.FromString,
                    response_serializer=chord__pb2.TSuccessResponse.SerializeToString,
            ),
            'populate_finger_table': grpc.unary_unary_rpc_method_handler(
                    servicer.populate_finger_table,
                    request_deserializer=chord__pb2.TPopulateFingerTableRequest.FromString,
                    response_serializer=chord__pb2.TPopulateFingerTableResponse.SerializeToString,
            ),
            'get_chord_info': grpc.unary_unary_rpc_method_handler(
                    servicer.get_chord_info,
                    request_deserializer=chord__pb2.TGetChordInfoRequest.FromString,
                    response_serializer=chord__pb2.TGetChordInfoResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Registry', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Registry(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def service_info(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Registry/service_info',
            chord__pb2.TEmpty.SerializeToString,
            chord__pb2.TSuccessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Registry/register',
            chord__pb2.TRegisterRequest.SerializeToString,
            chord__pb2.TRegisterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deregister(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Registry/deregister',
            chord__pb2.TDeregisterRequest.SerializeToString,
            chord__pb2.TSuccessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def populate_finger_table(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Registry/populate_finger_table',
            chord__pb2.TPopulateFingerTableRequest.SerializeToString,
            chord__pb2.TPopulateFingerTableResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_chord_info(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Registry/get_chord_info',
            chord__pb2.TGetChordInfoRequest.SerializeToString,
            chord__pb2.TGetChordInfoResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class NodeStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.service_info = channel.unary_unary(
                '/Node/service_info',
                request_serializer=chord__pb2.TEmpty.SerializeToString,
                response_deserializer=chord__pb2.TSuccessResponse.FromString,
                )
        self.register = channel.unary_unary(
                '/Node/register',
                request_serializer=chord__pb2.TGetFingerTableRequest.SerializeToString,
                response_deserializer=chord__pb2.TGetFingerTableResponse.FromString,
                )
        self.save = channel.unary_unary(
                '/Node/save',
                request_serializer=chord__pb2.TSaveRequest.SerializeToString,
                response_deserializer=chord__pb2.TSuccessResponse.FromString,
                )
        self.find = channel.unary_unary(
                '/Node/find',
                request_serializer=chord__pb2.TKeyRequest.SerializeToString,
                response_deserializer=chord__pb2.TSuccessResponse.FromString,
                )
        self.remove = channel.unary_unary(
                '/Node/remove',
                request_serializer=chord__pb2.TKeyRequest.SerializeToString,
                response_deserializer=chord__pb2.TSuccessResponse.FromString,
                )


class NodeServicer(object):
    """Missing associated documentation comment in .proto file."""

    def service_info(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def register(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def save(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def find(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def remove(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NodeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'service_info': grpc.unary_unary_rpc_method_handler(
                    servicer.service_info,
                    request_deserializer=chord__pb2.TEmpty.FromString,
                    response_serializer=chord__pb2.TSuccessResponse.SerializeToString,
            ),
            'register': grpc.unary_unary_rpc_method_handler(
                    servicer.register,
                    request_deserializer=chord__pb2.TGetFingerTableRequest.FromString,
                    response_serializer=chord__pb2.TGetFingerTableResponse.SerializeToString,
            ),
            'save': grpc.unary_unary_rpc_method_handler(
                    servicer.save,
                    request_deserializer=chord__pb2.TSaveRequest.FromString,
                    response_serializer=chord__pb2.TSuccessResponse.SerializeToString,
            ),
            'find': grpc.unary_unary_rpc_method_handler(
                    servicer.find,
                    request_deserializer=chord__pb2.TKeyRequest.FromString,
                    response_serializer=chord__pb2.TSuccessResponse.SerializeToString,
            ),
            'remove': grpc.unary_unary_rpc_method_handler(
                    servicer.remove,
                    request_deserializer=chord__pb2.TKeyRequest.FromString,
                    response_serializer=chord__pb2.TSuccessResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Node', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Node(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def service_info(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Node/service_info',
            chord__pb2.TEmpty.SerializeToString,
            chord__pb2.TSuccessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Node/register',
            chord__pb2.TGetFingerTableRequest.SerializeToString,
            chord__pb2.TGetFingerTableResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def save(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Node/save',
            chord__pb2.TSaveRequest.SerializeToString,
            chord__pb2.TSuccessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def find(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Node/find',
            chord__pb2.TKeyRequest.SerializeToString,
            chord__pb2.TSuccessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def remove(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Node/remove',
            chord__pb2.TKeyRequest.SerializeToString,
            chord__pb2.TSuccessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)