#!/usr/bin/env python

import argparse
import os
import sys
import time
import signal

import grpc
from concurrent import futures

import bmi_pb2_grpc
from bmi_grpc_server import BmiServer

"""
Run server script, turning a BMI implementation into an executable by looping indefinitely, until interrupt signals are
handled. The command line tool needs at least a module and class name to instantiate the BMI wrapper class that exposes
the implementation to other processes.
"""

ENV_BMI_PACKAGE = "BMI_PACKAGE"
ENV_BMI_MODULE = "BMI_MODULE"
ENV_BMI_CLASS = "BMI_CLASS"

kill_server = False


def interrupt(signum, frame):
    global kill_server
    kill_server = True


def serve(class_name, module_name, package_name, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bmi_pb2_grpc.add_BmiServiceServicer_to_server(BmiServer(class_name, module_name, package_name), server)
    server.add_insecure_port("[::]:" + str(port))
    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGABRT, interrupt)
    signal.signal(signal.SIGTERM, interrupt)
    server.start()
    try:
        while not kill_server:
            time.sleep(0.1)
        server.stop(0)
    except KeyboardInterrupt:
        server.stop(0)


def main():
    parser = argparse.ArgumentParser(description="BMI GRPC server runner",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--name", "-n", metavar="PACKAGE.MODULE.CLASS", type=str,
                        help="Full name of the BMI implementation class. The module should be in your python search "
                             "path and the class should have a constructor with no arguments")
    parser.add_argument("--port", "-p", metavar="N", default=50051, type=int,
                        help="Network port for the GRPC server and client")
    parser.add_argument("--path", "-d", metavar="DIR", default=None, type=str,
                        help="Extra path name to append to the server instance process")

    args = parser.parse_args()
    if args.path is not None:
        sys.path.append(args.path)

    parts = "" if args.name is None else args.name.split('.')
    class_name = parts[-1] if len(parts) > 0 else ""
    if not class_name:
        class_name = os.environ.get(ENV_BMI_CLASS, "")
    if not class_name:
        raise ValueError("Missing bmi implementation: class could not be derived from name input %s or environment "
                         "variable %s" % (args.name, ENV_BMI_CLASS))
    module_name = parts[-2] if len(parts) > 1 else ""
    if not module_name:
        module_name = os.environ.get(ENV_BMI_MODULE, "")
    if not module_name:
        raise ValueError("Missing module name: module could not be derived from name input %s or environment "
                         "variable %s" % (args.name, ENV_BMI_MODULE))
    package_name = '.'.join(parts[:-2]) if len(parts) > 2 else None
    serve(class_name, module_name, package_name, args.port)


if __name__ == "__main__":
    main()
