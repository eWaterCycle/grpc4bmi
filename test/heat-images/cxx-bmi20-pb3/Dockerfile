# Build with
#
#  docker build -t heat:py-2.0 test/heat-images/cxx-bmi20-pb3
#
FROM debian:buster AS builder

RUN apt update && apt install -qy git build-essential cmake autoconf libtool pkg-config libssl-dev

# Compile gRPC
WORKDIR /opt/grpc

ARG GRPC_VERSION=v1.51.1
RUN echo ${GRPC_VERSION}
RUN git clone -b ${GRPC_VERSION} https://github.com/grpc/grpc .
RUN git submodule update --init
RUN mkdir -p cmake/build 

WORKDIR /opt/grpc/cmake/build

RUN cmake -DgRPC_INSTALL=ON  -DgRPC_SSL_PROVIDER=package -DgRPC_BUILD_TESTS=OFF -DBUILD_SHARED_LIBS=ON ../..
RUN make -j6 && make install

# Install bmi-cxx
WORKDIR /opt/bmi-cxx
ARG BMI_VERSION=v2.0
RUN git clone -b ${BMI_VERSION} https://github.com/csdms/bmi-cxx .
RUN mkdir _build && cd _build && cmake .. && make install

# Fetch heat-cxx
WORKDIR /opt/bmi-example-cxx

ARG HEAT_VERSION=v2.1
RUN git clone -b ${HEAT_VERSION} https://github.com/csdms/bmi-example-cxx .
RUN mkdir _build && cd _build && cmake .. && make install

WORKDIR /opt/run_heat_bmi_model 

# grpc4bmi
WORKDIR /opt/grpc4bmi
RUN git clone -b bmi2  https://github.com/eWaterCycle/grpc4bmi .
RUN git submodule update --init
WORKDIR /opt/grpc4bmi/cpp
RUN mkdir build && cd build && cmake .. && make install

WORKDIR /opt/grpc4bmiheatcxx

# Add main
COPY run_heat_bmi_model.cc /opt/run_heat_bmi_model/grpc
COPY CMakeLists.txt /opt/run_heat_bmi_model/grpc

# Compile
RUN mkdir build && cd build && cmake .. && make install

# run container
FROM debian:buster

# Copy compiled and deps over
COPY --from=builder /opt/bmi-example-cxx-2.1/run_heat_bmi_model /bin/run_heat_bmi_model

ENTRYPOINT ["/bin/run_heat_bmi_model"]
