# DockerFile for grpc4bmi. Installs the C++ bindings in the /usr/local prefix directory in the container. If you are
# planning to run a container with your BMI-enabled model and communicate with it using grpc4bmi, you can use this as a
# base image for your model
FROM ubuntu:24.04
LABEL maintainer="eWaterCycle <ewatercycle@esciencecenter.nl>"
LABEL org.opencontainers.image.source="https://github.com/eWaterCycle/grpc4bmi"

ENV GRPC_VERSION="1.66.1"
ENV BMIC_VERSION="2.1.2"
ENV BMICXX_VERSION="2.0.2"

# Prerequisite packages
RUN apt-get update && apt-get install -y \
    automake \
    build-essential \
    cmake \
    curl \
    g++ \
    gfortran \
    git \
    libtool \
    libssl-dev \
    make \
    pkg-config \
    vim-tiny \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Build grpc from source (removing git history saves 1.7 GB)
RUN git clone --branch v${GRPC_VERSION} --depth 1 --recurse-submodules https://github.com/grpc/grpc /opt/grpc && \
    rm -rf /opt/grpc/.git
WORKDIR /opt/grpc/cmake/_build
RUN cmake ../.. \
        -DgRPC_INSTALL=ON \
        -DgRPC_SSL_PROVIDER=package \
        -DgRPC_BUILD_TESTS=OFF \
        -DCMAKE_CXX_STANDARD=17 \
        -DBUILD_SHARED_LIBS=ON && \
    make install && \
    make clean

# Build bmi-c and bmi-cxx from source
RUN git clone --branch v${BMIC_VERSION} https://github.com/csdms/bmi-c /opt/bmi-c
WORKDIR /opt/bmi-c/_build
RUN cmake .. && \
    make install && \
    make clean
RUN git clone --branch v${BMICXX_VERSION} https://github.com/csdms/bmi-cxx /opt/bmi-cxx
WORKDIR /opt/bmi-cxx/_build
RUN cmake .. && \
    make install && \
    make clean

RUN ldconfig

# Build grpc4bmi from source
COPY . /opt/grpc4bmi
WORKDIR /opt/grpc4bmi/cpp/_build
RUN cmake .. -DCMAKE_CXX_STANDARD=17 && \
    make && \
    ctest && \
    make install && \
    make clean

WORKDIR /opt
