from oaas_transport_grpc.rpc import call_pb2
from oaas_transport_grpc.rpc import call_pb2_grpc


class ServiceInvokerProxy(call_pb2_grpc.ServiceInvokerServicer):
    """
    Invokes the service on this server.
    """
    def InvokeMethod(self, request, context) -> call_pb2.Data:
        raise Exception("method is getting called")
        return call_pb2.Data(s="abc")
