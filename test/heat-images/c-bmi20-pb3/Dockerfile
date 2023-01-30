# Build with
#
#  docker build -t heat:c-bmi20-pb3 -f test/heat-images/c-bmi20-pb3/Dockerfile .
#
# Run with
#
# ipython
# from grpc4bmi.bmi_client_docker import BmiClientDocker
# model = BmiClientDocker('heat:c-bmi20-pb3', work_dir='/tmp', delay=1)
# model.get_component_name()
# model.get_output_var_names()
# from pathlib import Path
# config = Path('/tmp/heat.config.txt')
# config.write_text('1.5, 8.0, 7, 6')
# model.initialize(str(config))
# model.update()
# import numpy as np
# model.get_value('plate_surface__temperature', np.zeros(42))
#
FROM debian:buster AS builder

# Install build deps
RUN apt-get update && apt-get install -qy git build-essential cmake autoconf libtool pkg-config libssl-dev

# Compile gRPC
WORKDIR /opt/grpc
ARG GRPC_VERSION=v1.51.1
RUN echo ${GRPC_VERSION}
RUN git clone -b ${GRPC_VERSION} --depth 1 https://github.com/grpc/grpc . && git submodule update --init
WORKDIR /opt/grpc/cmake/build
RUN cmake -DgRPC_INSTALL=ON  -DgRPC_SSL_PROVIDER=package -DgRPC_BUILD_TESTS=OFF -DBUILD_SHARED_LIBS=ON ../.. \
    && make -j6 && make install && ldconfig

# Install bmi-cxx
ARG BMICXX_VERSION=v2.0
RUN git clone -b ${BMICXX_VERSION} https://github.com/csdms/bmi-cxx.git /opt/bmi-cxx
WORKDIR /opt/bmi-cxx/build
RUN cmake .. && make install

# Install bmi-c
ARG BMIC_VERSION=v2.1
RUN git clone -b ${BMIC_VERSION} https://github.com/csdms/bmi-c.git /opt/bmi-c
WORKDIR /opt/bmi-c/build
RUN cmake .. && make install

# Install heat-c
ARG HEAT_VERSION=v2.0.1
RUN git clone -b ${HEAT_VERSION} https://github.com/csdms/bmi-example-c /opt/bmi-example-c
WORKDIR /opt/bmi-example-c/build
RUN cmake .. && make install && ldconfig

# Install grpc4bmi, use locally cloned repo
WORKDIR /opt/grpc4bmi
COPY cpp/ /opt/grpc4bmi/cpp/
COPY proto/ /opt/grpc4bmi/proto/
RUN rm -rf /opt/grpc4bmi/cpp/build
WORKDIR /opt/grpc4bmi/cpp/build
RUN cmake .. && make install

# Compile main
WORKDIR /opt/grpc4bmiheatc/build
COPY test/heat-images/c-bmi20-pb3/run_bmi_server.cc /opt/grpc4bmiheatc
COPY test/heat-images/c-bmi20-pb3/CMakeLists.txt /opt/grpc4bmiheatc
RUN cmake .. && make install

# run container
FROM debian:buster

# Install runtime deps
RUN apt-get update && apt-get install -qy libssl1.1 && rm -rf /var/lib/apt/lists/*

# Copy compiled and deps
COPY --from=builder /usr/local/bin/run_bmi_server /usr/local/bin/run_bmi_server
COPY --from=builder /usr/local/lib/ /usr/local/lib/

RUN ldconfig

ENV BMI_PORT=50051

ENTRYPOINT ["/usr/local/bin/run_bmi_server"]
