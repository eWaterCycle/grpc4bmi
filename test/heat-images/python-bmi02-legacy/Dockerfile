# Python heat model with BMI v0.2, grpc4bmi==bmi2 and pb3
#
# Build with
#
#   docker build -t heat:py-0.2-legacy test/heat-images/python-bmi02-legacy
#
#
# Run with
#
#   from grpc4bmi.bmi_client_docker import BmiClientDocker
#   model = BmiClientDocker('heat:py-0.2-legacy', work_dir='/tmp', delay=1)
#

FROM python:3.10-buster

RUN pip install numpy 'scipy==1.8.1' 'PyYAML<6'

RUN pip install https://github.com/csdms/bmi-example-python/archive/refs/tags/v0.1.zip

RUN pip install https://github.com/eWaterCycle/grpc4bmi/archive/refs/heads/bmi2.zip

ENTRYPOINT ["run-bmi-server","--bmi-version", "0.2", "--name", "heat.BmiHeat", "--port", "50051"]
