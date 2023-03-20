# Python heat model with BMI v2.0 and pb3
#
# Build with
#
#   docker build -t heat:py-2.0 test/heat-images/python-bmi20
#
#
# Run with

#   from grpc4bmi.bmi_client_docker import BmiClientDocker
#   model = BmiClientDocker('heat:py-2.0', work_dir='/tmp', delay=1)
#
# docker run -ti --entrypoint pip heat:py-2.0 list |grep grpc
# grpc4bmi                 0.3.2
# grpcio                   1.51.1
# grpcio-reflection        1.48.2
# grpcio-status            1.48.2
# docker run -ti --entrypoint pip heat:py-2.0 list |grep proto
# googleapis-common-protos 1.58.0
# protobuf                 3.20.3

FROM python:3.10-buster

RUN pip install https://github.com/csdms/bmi-example-python/archive/44c7d4c54f7fa4c17f51f86a645ba3e2633a4dfb.zip

# Install grpc4bmi, use commit c5cc9b9bf33b6043e8db242a07c6fb92b9c63f66
# head of bmi2 branch, PR https://github.com/eWaterCycle/grpc4bmi/pull/124
RUN pip install https://github.com/eWaterCycle/grpc4bmi/archive/c5cc9b9bf33b6043e8db242a07c6fb92b9c63f66.zip

ENTRYPOINT ["run-bmi-server", "--name", "heat.BmiHeat", "--port", "50051"]
