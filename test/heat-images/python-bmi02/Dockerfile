# Python heat model with BMI v0.2, grpc4bmi==0.2 and pb3
#
# Build with
#
#   docker build -t heat:py-0.2 test/heat-images/python-bmi02
#
#
# Run with

#   from grpc4bmi.bmi_client_docker import BmiClientDocker
#   model = BmiClientDocker('heat:py-0.2', work_dir='/tmp', delay=1)
#

# docker run -ti --entrypoint pip heat:py-0.2 list |grep grpc
# grpc4bmi                 0.2.16
# grpcio                   1.51.1
# grpcio-reflection        1.48.2
# docker run -ti --entrypoint pip heat:py-0.2 list |grep proto
# protobuf                 3.20.3

FROM python:3.10-buster

RUN pip install numpy 'scipy==1.8.1' 'PyYAML<6'

RUN pip install https://github.com/csdms/bmi-example-python/archive/refs/tags/v0.1.zip

RUN pip install grpc4bmi==0.2.16

ENTRYPOINT ["run-bmi-server", "--name", "heat.BmiHeat", "--port", "50051"]
