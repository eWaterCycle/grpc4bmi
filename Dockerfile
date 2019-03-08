# DockerFile for grpc4bmi
FROM ubuntu:bionic
MAINTAINER Gijs van den Oord <g.vandenoord@esciencecenter.nl>
RUN apt-get update

# Prerequisite packages
RUN apt-get install -y wget git build-essential g++ make cmake curl automake libtool pkg-config

# Build grpc from source
RUN git clone -b $(curl -L https://grpc.io/release) --depth=1 https://github.com/grpc/grpc /opt/grpc
WORKDIR /opt/grpc
RUN git submodule update --init --recursive
RUN make install
WORKDIR third_party/protobuf
RUN make install

# Build bmi-c from source
RUN git clone --depth=1 https://github.com/eWaterCycle/grpc4bmi.git /opt/grpc4bmi
WORKDIR /opt/grpc4bmi
RUN git submodule update --init --recursive
RUN mkdir -p /opt/grpc4bmi/cpp/bmi-c/build
WORKDIR /opt/grpc4bmi/cpp/bmi-c/build
RUN cmake ..
RUN make install

# Build grpc4bmi from source
RUN mkdir -p /opt/grpc4bmi/cpp/build
WORKDIR /opt/grpc4bmi/cpp/build
RUN cmake ..
RUN make install

ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/lib"
ENV PATH="${PATH}:/usr/local/bin"
