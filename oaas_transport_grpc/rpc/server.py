import logging
from concurrent import futures

import grpc

from oaas_transport_grpc.rpc import call_pb2
from oaas_transport_grpc.rpc import call_pb2_grpc


class Wut(call_pb2_grpc.ServiceInvokerServicer):
    def InvokeMethod(self, request, context) -> call_pb2.Data:
        return call_pb2.Data(s="abc")


def create_server(server_address):
    server = grpc.server(futures.ThreadPoolExecutor())
    call_pb2_grpc.add_ServiceInvokerServicer_to_server(Wut(), server)
    port = server.add_insecure_port(server_address)
    return server, port


def serve(server):
    server.start()
    server.wait_for_termination()


def main():
    server, unused_port = create_server('[::]:50051')
    serve(server)


if __name__ == '__main__':
    logging.basicConfig()
    main()
