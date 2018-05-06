import os
import subprocess

from grpc4bmi.bmi_grpc_client import BmiClient


class BmiClientSubProcess(BmiClient):

    def __init__(self, module_name):
        port = BmiClient.get_unique_port()
        name_options = ["--name", module_name]
        port_options = ["--port", str(port)]
        self.pipe = subprocess.Popen(["run-bmi-server"] + name_options + port_options, env=dict(os.environ))
        super(BmiClientSubProcess, self).__init__(BmiClient.create_grpc_channel(port=p))

    def __del__(self):
        self.pipe.terminate()

    def get_value_ref(self, var_name):
        raise NotImplementedError("Cannot exchange memory referenecs accross process boundary")
