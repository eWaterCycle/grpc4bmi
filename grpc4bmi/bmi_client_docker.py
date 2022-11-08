import os
import time
from os.path import abspath
from typing import Iterable

import docker
from typeguard import check_argument_types, qualified_name

from grpc4bmi.bmi_grpc_client import BmiClient
from grpc4bmi.exceptions import DeadContainerException


class BmiClientDocker(BmiClient):
    """
    BMI gRPC client for dockerized server processes: the initialization launches the docker container which should have the
    run-bmi-server as its command. Also, it should expose the tcp port 50001 for communication with this client. Upon
    destruction, this class terminates the corresponding docker server.


    Args:
        image (str): Docker image name of grpc4bmi wrapped model
        image_port (int): Port of server inside the image
        host (str): Host on which the image port is published on a random port
        input_dirs (Iterable[str]): Directories for input files of model.

            All of directories will be mounted read-only inside Docker container on same path as outside container.

        work_dir (str): Working directory for model.

            Directory is mounted inside container and changed into.

        user (str): Username or UID of Docker container. Defaults to own UID.
        remove (bool): Automatically remove the container and logs when it exits.

            Enable to get logs when container dies prematurely.

        delay (int): Seconds to wait for Docker container to startup, before connecting to it

            Increase when container takes a long time to startup.

        timeout (int): Seconds to wait for gRPC client to connect to server.

            By default will try forever to connect to gRPC server inside container.
            Set to low number to escape endless wait.

    See :py:class:`grpc4bmi.bmi_client_apptainer.BmiClientApptainer` for examples using `input_dirs` and `work_dir`.
    """

    def __init__(self, image: str, work_dir: str, image_port=50051, host=None,
                 input_dirs: Iterable[str] = tuple(),
                 user=os.getuid(), remove=False, delay=5,
                 timeout=None):
        assert check_argument_types()
        if type(input_dirs) == str:
            msg = f'type of argument "input_dirs" must be collections.abc.Iterable; ' \
                  f'got {qualified_name(input_dirs)} instead'
            raise TypeError(msg)
        port = BmiClient.get_unique_port()
        client = docker.from_env()
        volumes = {}
        for raw_input_dir in input_dirs:
            input_dir = abspath(raw_input_dir)
            if not os.path.isdir(input_dir):
                raise NotADirectoryError(input_dir)
            volumes[input_dir] = {"bind": input_dir, "mode": "ro"}

        self.work_dir = abspath(work_dir)
        if self.work_dir in volumes:
            raise ValueError('Found work_dir equal to one of the input directories. Please drop that input dir.')
        if not os.path.isdir(self.work_dir):
            raise NotADirectoryError(self.work_dir)
        volumes[self.work_dir] = {"bind": self.work_dir, "mode": "rw"}
        self.container = client.containers.run(image,
                                               ports={str(image_port) + "/tcp": port},
                                               volumes=volumes,
                                               working_dir=self.work_dir,
                                               user=user,
                                               remove=remove,
                                               detach=True)
        time.sleep(delay)
        if not remove:
            # Only able to reload, read logs when container is not in auto remove mode
            self.container.reload()
            if self.container.status == 'exited':
                exitcode = self.container.attrs["State"]["ExitCode"]
                logs = self.logs()
                msg = f'Failed to start Docker container with image {image}, Container log: {logs}'
                raise DeadContainerException(msg, exitcode, logs)

        super(BmiClientDocker, self).__init__(BmiClient.create_grpc_channel(port=port, host=host), timeout=timeout)

    def __del__(self):
        if hasattr(self, "container"):
            self.container.stop()

    def get_value_ref(self, var_name):
        raise NotImplementedError("Cannot exchange memory references across process boundary")

    def logs(self) -> str:
        """Returns complete combined stdout and stderr written by the Docker container.
        """
        if hasattr(self, "container"):
            return self.container.logs().decode('utf8')
        return ''
