[![DOI](https://zenodo.org/badge/130237165.svg)](https://zenodo.org/badge/latestdoi/130237165)

# grpc4bmi

## Purpose

This software allows you to wrap your BMI implementation (https://github.com/csdms/bmi) in a server process and communicate with it via the included python client. The communication is serialized to protocol buffers by GRPC (https://grpc.io/) and occurs over network ports.

## Installation

Optionally, create your virtual environment and activate it, Then, run
```
pip install grpc4bmi
```
on the client (python) side. If your server model is implemented in Python, do the same in the server environment (e.g. docker container). If the model is implemented in R, run instead
```bash
pip install grpc4bmi[R]
```
in the server environment. For bleeding edge version from GitHub use
```bash
pip install git+https://github.com/eWaterCycle/grpc4bmi.git#egg=grpc4bmi
```
Finally if the model is implemented in C or C++, clone this git repo and run
```bash
make ; make install
```
in the cpp folder.

## Usage

### Model written in Python
For inspiration look at the example in the test directory. To start a server process that allows calls to your BMI implementation, type
```bash
run-bmi-server --name <PACKAGE>.<MODULE>.<CLASS> --port <PORT> --path <PATH>
```
where ```<PACKAGE>, <MODULE>``` are the python package and module containing your implementation, ```<CLASS>``` is your 
bmi model class name, ```<PORT>``` is any available port on the host system, and optionally ```<PATH>``` denotes an 
additional path that should be added to the system path to make your implementation work. The name option above is 
optional, and if not provided the script will look at the environment variables ```BMI_PACKAGE```, ```BMI_MODULE``` and 
```BMI_CLASS```. Similarly, the port can be defined by the environment variable ```BMI_PORT```.
This software assumes that your implementation constructor has no parameters.

### Model written in C/C++ (beta)
Create an executable along the lines of cpp/run-bmi-server.cc. You can copy the file and replace the function
```C++
Bmi* create_model_instance()
{
    /* Return your new BMI instance pointer here... */
}
```
with the instantiation of your model BMI. The model needs to implement the csdms BMI for C, but you may also implement our more object-oriented C++ interface [BmiCppExtension](https://github.com/eWaterCycle/grpc4bmi/blob/master/cpp/bmi_cpp_extension.h).

### Model written in R
The grpc4bmi Python package can also run BMI models written in R if the model is a subclass of [AbstractBmi](https://github.com/eWaterCycle/bmi-r/blob/master/R/abstract-bmi.R#L9)
See https://github.com/eWaterCycle/bmi-r for instruction on R and Docker.

Run the R model a server with
```bash
run-bmi-server --lang R [--path <R file with BMI model>] --name [<PACKAGE>::]<CLASS> --port <PORT>
```

For example with [WALRUS](https://github.com/eWaterCycle/grpc4bmi-examples/tree/master/walrus) use
```bash
run-bmi-server --lang R --path ~/git/eWaterCycle/grpc4bmi-examples/walrus/walrus-bmi.r --name WalrusBmi --port 50051
```

### The client side
The client side has only a Python implementation. The default BMI client assumes a running server process on a given port.
```python
from grpc4bmi.bmi_grpc_client import BmiClient
mymodel = BmiClient(grpc.insecure_channel("localhost:<PORT>"))
print mymodel.get_component_name()
mymodel.initialize(<FILEPATH>)
...further BMI calls...
```

The package contains also client implementation that own the server process, either as a python subprocess or a docker 
image running the ```run-bmi-server``` script. For instance
```python
from grpc4bmi.bmi_client_subproc import BmiClientSubProcess
mymodel = BmiClientSubProcess(<PACKAGE>.<MODULE>.<CLASS>)
```
will automatically launch the server in a sub-process and
```python
from grpc4bmi.bmi_client_subproc import BmiClientDocker
mymodel = BmiClientDocker(<IMAGE>,<PORT>)

```
will launch a docker container, assuming that a GRPC BMI server will start and exposes the port ```<PORT>```.

## Development: generating the grpc code

When developers change the proto-file, it is necessary to install grpc tools python packages in your python environment:
```bash
pip install -r requirements.txt
pip install -e .
# For R integration also install the R extras with
pip install -e .[R]

```
and install the C++ runtime and `protoc` command as described in <https://github.com/google/protobuf/blob/master/src/README.md>.
After this, simply executing the `proto_gen.sh` script should do the job. 

## Future work

More language bindings are underway.
