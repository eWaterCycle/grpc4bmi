# grpc4bmi

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1462641.svg)](https://doi.org/10.5281/zenodo.1462641)
[![CI](https://github.com/eWaterCycle/grpc4bmi/workflows/CI/badge.svg)](https://github.com/eWaterCycle/grpc4bmi/actions?query=workflow%3ACI)
[![Documentation Status](https://readthedocs.org/projects/grpc4bmi/badge/?version=latest)](https://grpc4bmi.readthedocs.io/en/latest/?badge=latest)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=grpc4bmi&metric=alert_status)](https://sonarcloud.io/dashboard?id=grpc4bmi)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=grpc4bmi&metric=coverage)](https://sonarcloud.io/dashboard?id=grpc4bmi)

## Purpose

This software allows you to wrap your [Basic Model Interface (BMI)](https://github.com/csdms/bmi) implementation in a server process and communicate with it via the included Python client. The communication is serialized to protocol buffers by [GRPC](https://grpc.io/) and occurs over network ports. Can run models in isolated containers using Docker or Apptainer.

## Installation

Optionally, create your virtual environment and activate it, Then, run

```bash
pip install grpc4bmi
```

on the client (Python) side. If your server model is implemented in Python, do the same in the server environment (e.g. docker container). If the model is implemented in R, run instead

```bash
pip install grpc4bmi[R]
```

If the model is implemented in Julia, run instead

```bash
pip install grpc4bmi[julia]
```

in the server environment. For bleeding edge version from GitHub use

```bash
pip install git+https://github.com/eWaterCycle/grpc4bmi.git#egg=grpc4bmi
```

Finally if the model is implemented in C or C++, clone this git repo and run

```bash
make
make install
```

in the cpp folder.

## Usage

### Model written in Python

A model should be a subclass of the `Bmi` class from the [bmipy](https://pypi.org/project/bmipy/2.0/) package.

For inspiration look at the [example](test/fake_models.py) in the test directory. 

To start a server process that allows calls to your BMI implementation, type

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

with the instantiation of your model BMI. The model needs to implement the csdms BMI for C, but you may also implement our more object-oriented C++ interface [BmiCppExtension](https://github.com/eWaterCycle/grpc4bmi/blob/main/cpp/bmi_cpp_extension.h).

### Model written in R

The grpc4bmi Python package can also run BMI models written in R if the model is a subclass of [AbstractBmi](https://github.com/eWaterCycle/bmi-r/blob/master/R/abstract-bmi.R#L9)
See [https://github.com/eWaterCycle/bmi-r](https://github.com/eWaterCycle/bmi-r) for instruction on R and Docker.

Run the R model a server with

```bash
run-bmi-server --lang R [--path <R file with BMI model>] --name [<PACKAGE>::]<CLASS> --port <PORT>
```

For example with [WALRUS](https://github.com/eWaterCycle/grpc4bmi-examples/tree/master/walrus) use

```bash
run-bmi-server --lang R --path ~/git/eWaterCycle/grpc4bmi-examples/walrus/walrus-bmi.r --name WalrusBmi --port 55555
```

### Models written in Julia

The grpc4bmi Python package can also run BMI models written in Julia if the model has an implementation of the [BasicModelInterface.jl](https://github.com/Deltares/BasicModelInterface.jl).

Run the Julia model in Python with

```bash
from grpc4bmi.bmi_julia_model import BmiJulia

mymodel = BmiJulia.from_name('<package>.<model>', 'BasicModelInterface')
```

For example with [Wflow.jl](https://github.com/Deltares/Wflow.jl/) use

```bash
# Install Wflow.jl package in the Julia environment managed by the juliacall Python package.
from juliacall import Main as jl
jl.Pkg.add("Wflow")
# Create the model
from grpc4bmi.bmi_julia_model import BmiJulia
mymodel = BmiJulia.from_name('Wflow.Model', 'Wflow.bmi.BMI')
```

A Julia model has to be run locally. It can not be run in the default gRPC client/server Docker container mode because:

1. Julia has no gRPC server implementation
2. Calling Julia methods from Python gRPC server causes 100% CPU usage and no progress
3. Calling Julia methods from C++ gRPC server causes segmentation faults

### The client side

The client side has only a Python implementation. The default BMI client assumes a running server process on a given port.

```python
from grpc4bmi.bmi_grpc_client import BmiClient
import grpc
mymodel = BmiClient(grpc.insecure_channel("localhost:<PORT>"))
print mymodel.get_component_name()
mymodel.initialize(<FILEPATH>)
...further BMI calls...
```

The package contains also client implementation that own the server process, either as a Python subprocess or a Docker
container or a Singularity container or a Apptainer container running the ```run-bmi-server``` script. For instance
```python
from grpc4bmi.bmi_client_subproc import BmiClientSubProcess
mymodel = BmiClientSubProcess(<PACKAGE>.<MODULE>.<CLASS>)
```

will automatically launch the server in a sub-process and

```python
from grpc4bmi.bmi_client_docker import BmiClientDocker
mymodel = BmiClientDocker(<IMAGE>, <WORK DIR TO MOUNT>, input_dirs=[<INPUT DIRECTORIES TO MOUNT>])
```
will launch a Docker container based on supplied Docker image
and will mount supplied directories to share files between the container and host.

```python
from grpc4bmi.bmi_client_singularity import BmiClientSingularity
mymodel = BmiClientSingularity(<IMAGE>, <WORK DIR TO MOUNT>, input_dirs=[<INPUT DIRECTORIES TO MOUNT>])
```
will launch a singularity container on based supplied Singularity image
and will mount supplied directories to share files between the container and host.

```python
from grpc4bmi.bmi_client_apptainer import BmiClientApptainer
mymodel = BmiClientApptainer(<IMAGE>, <WORK DIR TO MOUNT>, input_dirs=[<INPUT DIRECTORIES TO MOUNT>])
```
will launch a Apptainer container on based supplied Apptainer image
and will mount supplied directories to share files between the container and host.

For more documentation see [https://grpc4bmi.readthedocs.io/](https://grpc4bmi.readthedocs.io/).

## Development: generating the gRPC code

When developers change the proto-file, it is necessary to install gRPC tools Python packages in your Python environment:

```bash
# Create virtual env
python3 -m venv .venv
. venv/bin/activate
# Make sure latest pip and wheel are install
pip install -U pip wheel
pip install -r dev-requirements.txt
# For R integration also install the R extras with
pip install -e .[R]
# For building docs (cd docs && make html) also install the docs extras with
pip install -e .[docs]
```

and install the C++ runtime and `protoc` command as described in <https://github.com/google/protobuf/blob/master/src/README.md>.
After this, simply executing the `proto_gen.sh` script should do the job.
