import os
import subprocess
import time

from grpc4bmi.bmi_grpc_client import BmiClient


class BmiClientSubProcess(BmiClient):

    """
    BMI GRPC client that owns its server process, i.e. initiates and destroys the BMI server upon its own construction or
    respective destruction. The server is a forked subprocess running the run_server command.

    >>> from grpc4bmi.bmi_client_subproc import BmiClientSubProcess
    >>> mymodel = BmiClientSubProcess(<PACKAGE>.<MODULE>.<CLASS>)
    """

    def __init__(self, module_name, path=None, timeout=None, delay=1):
        host = "localhost"
        port = BmiClient.get_unique_port(host)
        name_options = ["--name", module_name]
        port_options = ["--port", str(port)]
        path_options = ["--path", path] if path else []
        self.pipe = subprocess.Popen(["run-bmi-server"] + name_options + port_options + path_options, env=dict(os.environ))
        time.sleep(delay)
        super(BmiClientSubProcess, self).__init__(BmiClient.create_grpc_channel(port=port, host=host), timeout=timeout)

    def __del__(self):
        self.pipe.kill()
        self.pipe.wait(timeout=0.1)

    def get_value_ref(self, var_name):
        raise NotImplementedError("Cannot exchange memory references across process boundary")
