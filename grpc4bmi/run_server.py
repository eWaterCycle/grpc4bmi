#!/usr/bin/env python

import argparse
import os
import sys
import time

import grpc
from concurrent import futures

import bmi_pb2_grpc
from bmi_grpc_server import BmiServer

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

ENV_BMI_MODULE = "BMI_MODULE"
ENV_BMI_CLASS = "BMI_CLASS"


def serve(module_name, class_name, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bmi_pb2_grpc.add_BmiServiceServicer_to_server(BmiServer(module_name, class_name), server)
    server.add_insecure_port("[::]:" + str(port))
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def main():
    parser = argparse.ArgumentParser(description="BMI GRPC server runner",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--name", "-n", metavar="MODULE.CLASS", default=".", type=str,
                        help="Full name of the BMI implementation class. The module should be in your python search "
                             "path and the class should have a constructor with no arguments")
    parser.add_argument("--port", "-p", metavar="N", default=50051, type=int,
                        help="Network port for the GRPC server and client")

    args = parser.parse_args()
    path = os.path.dirname(args.name)
    if path:
        sys.path.append(path)
    fname = os.path.basename(args.name)
    parts = fname.split('.')
    cls = parts[-1]
    if not cls:
        cls = os.environ.get(ENV_BMI_CLASS, "")
    if not cls:
        raise ValueError("Missing bmi implementation: class could not be derived from name input %s or environment "
                         "variable %s" % (args.name, ENV_BMI_CLASS))
    mod = '.'.join(parts[:-1])
    if not mod:
        mod = os.environ.get(ENV_BMI_MODULE, "")
    if not mod:
        raise ValueError("Missing module name: module could not be derived from name input %s or environment "
                         "variable %s" % (args.name, ENV_BMI_MODULE))
    serve(mod, cls, args.port)


if __name__ == "__main__":
    main()
