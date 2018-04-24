#!/usr/bin/env python

import argparse
import os
import time

import grpc
from concurrent import futures

import bmi_pb2_grpc
from bmi_grpc_server import BmiServer

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def serve(modulename, classname):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bmi_pb2_grpc.add_BmiServiceServicer_to_server(BmiServer(modulename, classname), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def main():
    parser = argparse.ArgumentParser(description="BMI GRPC server runner",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--module", metavar="NAME", type=str, help="Module name containing the BMI implementation "
                                                                   "class. This module should be in your python "
                                                                   "search path")
    parser.add_argument("--class", metavar="NAME", type=str, help="BMI implementation class containing your model. "
                                                                  "This class should have a constructor without "
                                                                  "arguments")
    args = parser.parse_args()
    modulename = getattr(args, "module", os.environ.get("BMI_MODULE", None))
    classname = getattr(args, "class", os.environ.get("BMI_CLASS", None))
    if modulename is None or classname is None:
        raise ValueError("Missing module and/or class name: either pass them as arguments or define the BMI_MODULE and "
                         "BMI_CLASS environment variables")
    serve(modulename, classname)


if __name__ == "__main__":
    main()

