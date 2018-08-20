#!/usr/bin/env bash

protoc -I ./proto --grpc_out=./cpp --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ./proto/bmi.proto
protoc -I ./proto --cpp_out=./cpp ./proto/bmi.proto
python -m grpc_tools.protoc -I./proto --python_out=./python/grpc4bmi --grpc_python_out=./python/grpc4bmi ./proto/bmi.proto
