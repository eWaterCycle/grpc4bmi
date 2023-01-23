# Build with
#
#  docker build -t heat:py-2.0 test/heat-images/cxx-bmi20-pb3
#
FROM debian:buster AS builder

RUN apt-get update && apt-get install -qy git build-essential cmake autoconf libtool pkg-config libssl-dev

# Compile gRPC
WORKDIR /opt/grpc

ARG GRPC_VERSION=v1.51.1
RUN echo ${GRPC_VERSION}
RUN git clone -b ${GRPC_VERSION} --depth 1 https://github.com/grpc/grpc . && git submodule update --init

WORKDIR /opt/grpc/cmake/build

RUN cmake -DgRPC_INSTALL=ON  -DgRPC_SSL_PROVIDER=package -DgRPC_BUILD_TESTS=OFF -DBUILD_SHARED_LIBS=ON ../.. \
    && make -j6 && make install && ldconfig

# grpc4bmi
WORKDIR /opt/grpc4bmi
RUN git clone -b latest-protobuf https://github.com/eWaterCycle/grpc4bmi .
RUN git submodule update --init
WORKDIR /opt/grpc4bmi/cpp/build
RUN cmake .. && make install

# Install bmi-cxx
WORKDIR /opt/grpc4bmi/cpp/bmi-cxx/build
RUN cmake .. && make install

# Install bmi-c
WORKDIR /opt/grpc4bmi/cpp/bmi-c/build
RUN cmake .. && make install

# Fetch heat-cxx
WORKDIR /opt/bmi-example-cxx

ARG HEAT_VERSION=v2.1
RUN git clone -b ${HEAT_VERSION} https://github.com/csdms/bmi-example-cxx .
WORKDIR /opt/bmi-example-cxx/build
RUN cmake .. && make install && ldconfig

WORKDIR /opt/grpc4bmiheatcxx/build

# Add main
COPY run_heat_bmi_model.cc /opt/grpc4bmiheatcxx
COPY CMakeLists.txt /opt/grpc4bmiheatcxx

# Compile
RUN cmake .. && make install

# run container
FROM debian:buster

# Copy compiled and deps over
COPY --from=builder /optgrpc4bmiheatcxx/build/run_heat_bmi_model /bin/run_heat_bmi_model

ENTRYPOINT ["/bin/run_heat_bmi_model"]
