# grpc4bmi
## Purpose
This software allows you to wrap your BMI implementation (https://github.com/csdms/bmi) in a server process and communicate with it via the included python client. The communication is serialized to protocol buffers by GRPC (https://grpc.io/) and occurs over network ports.

## Installation
Optionally, create your virtual environment and activate it, Then, run in the top-level directory
```
pip install -r requirements.txt
python setup.py install
```

## Usage
For inspiration look at the example in the test directory. To start a server process that allows calls to your BMI implementation, type
```
run-bmi-server --name <PACKAGE>.<MODULE>.<CLASS> --port <PORT> --path <PATH>
```
where ```<PACKAGE>, <MODULE>``` are the python package and module containing your implementation, ```<CLASS>``` is your 
bmi model class name, ```<PORT>``` is any available port on the host system, and optionally ```<PATH>``` denotes an 
additional path that should be added to the system path to make your implementation work. The name option above is 
optional, and if not provided the script will look at the environment variables ```BMI_PACKAGE```, ```BMI_MODULE``` and 
```BMI_CLASS```. Similarly, the port can be defined by the environment variable ```BMI_PORT```.
This software assumes that your implementation constructor has no parameters.
 
Now connect to this process by running python in another terminal and executing
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
## Future work
More language bindings are underway.
