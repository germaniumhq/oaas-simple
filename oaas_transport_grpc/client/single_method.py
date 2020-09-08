import json
from typing import Any, Union

from oaas import ClientDefinition

from oaas_transport_grpc.rpc import call_pb2


def create_data(data: Union[str, bytes, Any]) -> call_pb2.Data:
    if isinstance(data, str):
        return call_pb2.Data(s=data)

    if isinstance(data, bytes):
        return call_pb2.Data(b=bytes)

    json_data = json.dumps(data)
    return call_pb2.Data(json=json_data)


class SingleMethod:
    def __init__(self, *,
                 stub: Any,
                 client_definition: ClientDefinition,
                 method_name: str):
        self.stub = stub
        self.client_definition = client_definition
        self.method = method_name

    def __call__(self, *args, **kwargs):
        parameters = []

        for arg in args:
            param = call_pb2.ServiceCallParam(
                name=None,
                data=create_data(arg)
            )
            parameters.append(param)

        for arg_name, arg in kwargs.items():
            param = call_pb2.ServiceCallParam(
                name=arg_name,
                data=create_data(arg)
            )
            parameters.append(param)

        response: call_pb2.Data = self.stub.InvokeMethod(call_pb2.ServiceCall(
            namespace=None,
            service=self.client_definition.name,
            version=None,
            method=self.method,
            parameters=parameters
        ))

        return response
