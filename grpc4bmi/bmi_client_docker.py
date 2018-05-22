import shutil
import os

import docker

from grpc4bmi.bmi_grpc_client import BmiClient


class BmiClientDocker(BmiClient):

    """
    BMI GRPC client for dockerized server processes: the initialization launches the docker container which should have the
    run-bmi-server as its command. Also, it should expose the tcp port 50001 for communication with this client. Upon
    destruction, this class terminates the corresponding docker server.
    """

    input_mount_point = "/data/input"
    output_mount_point = "/data/output"

    def __init__(self, image, image_port=50051, host=None, input_dir=None, output_dir=None):
        port = BmiClient.get_unique_port()
        super(BmiClientDocker, self).__init__(BmiClient.create_grpc_channel(port=port, host=host))
        client = docker.from_env()
        volumes = {}
        self.input_dir = None
        if input_dir is not None:
            self.input_dir = os.path.abspath(input_dir)
            volumes[self.input_dir] = {"bind": BmiClientDocker.input_mount_point, "mode": "rw"}
        self.output_dir = None
        if output_dir is not None:
            self.output_dir = os.path.abspath(output_dir)
            volumes[self.output_dir] = {"bind": BmiClientDocker.output_mount_point, "mode": "rw"}
        self.container = client.containers.run(image, ports={str(image_port) + "/tcp": port},
                                               volumes=volumes,
                                               detach=True)

    def __del__(self):
        if hasattr(self,"container"):
            self.container.stop()

    def initialize(self, filename):
        if self.input_dir is not None:
            shutil.copy(filename, self.input_dir)
            fname = os.path.basename(filename)
            super(BmiClientDocker, self).initialize(os.path.join(BmiClientDocker.input_mount_point, fname))
        else:
            super(BmiClientDocker, self).initialize(filename)

    def get_value_ref(self, var_name):
        raise NotImplementedError("Cannot exchange memory references across process boundary")
