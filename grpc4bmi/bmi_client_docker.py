import os
import errno
import time

import docker

from grpc4bmi.bmi_grpc_client import BmiClient
from grpc4bmi.utils import stage_config_file


class BmiClientDocker(BmiClient):
    """
    BMI GRPC client for dockerized server processes: the initialization launches the docker container which should have the
    run-bmi-server as its command. Also, it should expose the tcp port 50001 for communication with this client. Upon
    destruction, this class terminates the corresponding docker server.


    Args:
        image (str): Docker image name of grpc4bmi wrapped model
        image_port (int): Port of server inside the image
        host (str): Host on which the image port is published on a random port
        input_dir (str): Directory for input files of model
        output_dir (str): Directory for input files of model
        user (str): Username or UID of Docker container
        remove (bool): Automatically remove the container when it exits

    """

    input_mount_point = "/data/input"
    output_mount_point = "/data/output"

    def __init__(self, image, image_port=50051, host=None,
                 input_dir=None, output_dir=None,
                 user=os.getuid(), remove=True):
        port = BmiClient.get_unique_port()
        client = docker.from_env()
        volumes = {}
        self.input_dir = None
        if input_dir is not None:
            self.input_dir = os.path.abspath(input_dir)
            volumes[self.input_dir] = {"bind": BmiClientDocker.input_mount_point, "mode": "rw"}
        self.output_dir = None
        if output_dir is not None:
            self.output_dir = os.path.abspath(output_dir)
            try:
                # Create output dir ourselves, otherwise Docker will create it as root user, resulting in permission
                # errors
                os.mkdir(self.output_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            volumes[self.output_dir] = {"bind": BmiClientDocker.output_mount_point, "mode": "rw"}
        self.container = client.containers.run(image,
                                               ports={str(image_port) + "/tcp": port},
                                               volumes=volumes,
                                               user=user,
                                               remove=remove,
                                               detach=True)
        time.sleep(5)
        super(BmiClientDocker, self).__init__(BmiClient.create_grpc_channel(port=port, host=host))

    def __del__(self):
        if hasattr(self, "container"):
            self.container.stop()

    def initialize(self, filename):
        fn = stage_config_file(filename, self.input_dir, self.input_mount_point)
        super(BmiClientDocker, self).initialize(fn)

    def get_value_ref(self, var_name):
        raise NotImplementedError("Cannot exchange memory references across process boundary")
