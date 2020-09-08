# Copyright 2019 The gRPC Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example handles rich error status in client-side."""

import logging

import grpc

from oaas_transport_grpc.rpc import call_pb2_grpc, call_pb2

_LOGGER = logging.getLogger(__name__)


def process(stub):
    try:
        response: call_pb2.Data = stub.InvokeMethod(call_pb2.ServiceCall(
            name="test"
        ))

        print(f"response is {response.s}")

        _LOGGER.info('Call success: %s', response)
    except grpc.RpcError as rpc_error:
        _LOGGER.error('Call failure: %s', rpc_error)


def main():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = call_pb2_grpc.ServiceInvokerStub(channel)
        process(stub)


if __name__ == '__main__':
    logging.basicConfig()
    main()
