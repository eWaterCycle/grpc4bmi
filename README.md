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
run-bmi-server --name <MODULE>.<CLASS> --port <PORT>
```
where ```<MODULE>``` is the python module containing your implementation, ```<CLASS>``` is your bmi model class name and ```<PORT>``` is any network port on your system. Now connect to this process from within python by
```
from grpc4bmi.bmi_grpc_client import BmiClient
mymodel = BmiClient(grpc.insecure_channel("localhost:<PORT>"))
print mymodel.get_component_name()
mymodel.initialize(<FILEPATH>)
...further BMI calls...
```

## Future work
More language bindings and support for dockerized server processes and are underway.
