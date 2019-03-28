Introduction
============

This software allows you to wrap your BMI implementation (https://github.com/csdms/bmi) in a server process and communicate with it via the included python client. The communication is serialized to protocol buffers by GRPC (https://grpc.io/) and occurs over network ports. On the server side, we support BMI implementations in :ref:`python <pythonservice>`, R or C/C++. Fortran models will need to be wrapped in C-implementation of the BMI. On the client side, we expose the python BMI (https://github.com/csdms/bmi-python/).

This setup enables you to wrap your BMI-enabled model in a container (https://www.docker.com/) and communicate with it from the host machine.