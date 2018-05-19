import shutil

import docker

from grpc4bmi.bmi_grpc_client import BmiClient


class BmiClientDocker(BmiClient):

    """
    BMI GRPC client for dockerized server processes: the initialization launches the docker container which should have the
    run-bmi-server as its command. Also, it should expose the tcp port 50001 for communication with this client. Upon
    destruction, this class terminates the corresponding docker server.
    """

    def __init__(self, image, image_port=50051, host=None, input_dir=None, output_dir=None):
        client = docker.from_env()
        port = BmiClient.get_unique_port()
        volumes = {}
        self.input_dir = input_dir
        if input_dir is not None:
            volumes[input_dir] = {"bind": "/data", "mode": "ro"}
        if output_dir is not None:
            volumes[output_dir] = {"bind": "/data/output", "mode": "rw"}
        self.container = client.containers.run(image, ports={image_port + "/tcp": port},
                                               volumes=volumes,
                                               detach=True)
        super(BmiClientDocker, self).__init__(BmiClient.create_grpc_channel(port=port, host=host))

    def __del__(self):
        self.container.stop()

    def initialize(self, filename):
        if self.input_dir is not None:
            shutil.copy(filename, self.input_dir)
            super(BmiClientDocker, self).initialize("/data/" + filename)
        else:
            super(BmiClientDocker, self).initialize(filename)

    def get_value_ref(self, var_name):
        raise NotImplementedError("Cannot exchange memory references across process boundary")
