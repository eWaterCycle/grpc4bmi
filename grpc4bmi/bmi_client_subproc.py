import grpc
import os

from grpc4bmi.bmi_grpc_client import BmiClient
import subprocess


class BmiClientSubProcess(BmiClient):

    def __init__(self, module_name):
        self.port = 50000
        name_options = ["--name", module_name]
        port_options = ["--port", str(self.port)]
        self.pipe = subprocess.Popen(["run-bmi-server"] + name_options + port_options, env=dict(os.environ))
        self.pipe.wait()
        super(BmiClientSubProcess, self).__init__(grpc.insecure_channel("localhost:" + str(self.port)))

    def __del__(self):
        self.pipe.terminate()

    def get_value_ref(self, var_name):
        raise NotImplementedError("Cannot exchange memory referenecs accross process boundary")
