# Build with
#
#  docker build -t heat:c-julia -f test/heat-images/c-julia/Dockerfile .
#
# Run with
#
# ipython
# from grpc4bmi.bmi_client_docker import BmiClientDocker
# model = BmiClientDocker('heat:c-julia', work_dir='/tmp', delay=1)
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
FROM julia:bullseye AS builder

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

# Install grpc4bmi, use commit c5cc9b9bf33b6043e8db242a07c6fb92b9c63f66
# head of bmi2 branch, PR https://github.com/eWaterCycle/grpc4bmi/pull/124
ARG GRPC4BMI_VERSION=c5cc9b9bf33b6043e8db242a07c6fb92b9c63f66
RUN git clone https://github.com/eWaterCycle/grpc4bmi /opt/grpc4bmi \
  && cd /opt/grpc4bmi && git checkout ${GRPC4BMI_VERSION}
WORKDIR /opt/grpc4bmi/cpp/build
RUN cmake .. && make install


# Compile main
WORKDIR /opt/grpc4bmiheatc-julia/build
COPY test/heat-images/c-julia/FindJulia.cmake /opt/grpc4bmiheatc-julia
COPY test/heat-images/c-julia/run_bmi_server.cc /opt/grpc4bmiheatc-julia
COPY test/heat-images/c-julia/CMakeLists.txt /opt/grpc4bmiheatc-julia
RUN cmake .. && make install

# run container
FROM julia:bullseye

# Install runtime deps
RUN apt-get update && apt-get install -qy libssl1.1 && rm -rf /var/lib/apt/lists/*

# Copy compiled and deps
COPY --from=builder /usr/local/bin/run_bmi_server /usr/local/bin/run_bmi_server
COPY --from=builder /usr/local/lib/ /usr/local/lib/

# Install heat-julia
RUN julia -e 'using Pkg; Pkg.add(url="https://github.com/csdms/bmi-example-julia.git",rev="80c34b4f2217599e600fe9372b1bae50e1229edf")'

RUN curl -L -O /usr/local/share/bmi/heat.toml https://github.com/csdms/bmi-example-julia/raw/main/example/heat.toml 

RUN echo '/usr/local/julia/lib' > /etc/ld.so.conf.d/julia.conf && ldconfig

ENV BMI_PORT=50051

ENTRYPOINT ["/usr/local/bin/run_bmi_server"]
