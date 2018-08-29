#!/usr/bin/env bash

protoc --cpp_out=./cpp --proto_path proto/grpc4bmi ./proto/grpc4bmi/bmi.proto
protoc --grpc_out=./cpp --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` --proto_path proto/grpc4bmi ./proto/grpc4bmi/bmi.proto
python -m grpc_tools.protoc -I./proto --python_out=./ --grpc_python_out=./ --proto_path proto ./proto/grpc4bmi/bmi.proto
