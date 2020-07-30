import os
import errno
import time

import docker

from grpc4bmi.bmi_grpc_client import BmiClient
from grpc4bmi.utils import stage_config_file


class DeadDockerContainerException(ChildProcessError):
    """
    Exception for when a Docker container has died.

    Args:
        message (str): Human readable error message
        exitcode (int): The non-zero exit code of the container
        logs (str): Logs the container produced

    """
    def __init__(self, message, exitcode, logs, *args):
        super().__init__(message, *args)
        #: Exit code of container
        self.exitcode = exitcode
        #: Stdout and stderr of container
        self.logs = logs


class BmiClientDocker(BmiClient):
    """
    BMI gRPC client for dockerized server processes: the initialization launches the docker container which should have the
    run-bmi-server as its command. Also, it should expose the tcp port 50001 for communication with this client. Upon
    destruction, this class terminates the corresponding docker server.


    Args:
        image (str): Docker image name of grpc4bmi wrapped model
        image_port (int): Port of server inside the image
        host (str): Host on which the image port is published on a random port
        input_dir (str): Directory for input files of model
        output_dir (str): Directory for input files of model
        user (str): Username or UID of Docker container
        remove (bool): Automatically remove the container and logs when it exits.
        delay (int): Seconds to wait for Docker container to startup, before connecting to it
        timeout (int): Seconds to wait for gRPC client to connect to server
        extra_volumes (Dict[str,Dict]): Extra volumes to attach to Docker container.

            The key is either the hosts path or a volume name and the value is a dictionary with the keys:

            - ``bind`` The path to mount the volume inside the container
            - ``mode`` Either ``rw`` to mount the volume read/write, or ``ro`` to mount it read-only.

            For example:

            .. code-block:: python

                    {'/data/shared/forcings/': {'bind': '/forcings', 'mode': 'ro'}}

    """

    input_mount_point = "/data/input"
    output_mount_point = "/data/output"

    def __init__(self, image, image_port=50051, host=None,
                 input_dir=None, output_dir=None,
                 user=os.getuid(), remove=False, delay=5,
                 timeout=None, extra_volumes=None):
        port = BmiClient.get_unique_port()
        client = docker.from_env()
        volumes = {}
        if extra_volumes is not None:
            volumes.update(extra_volumes)
        self.input_dir = None
        if input_dir is not None:
            self.input_dir = os.path.abspath(input_dir)
            if not os.path.isdir(self.input_dir):
                raise NotADirectoryError(input_dir)
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
        time.sleep(delay)
        if not remove:
            # Only able to reload, read logs when container is not in auto remove mode
            self.container.reload()
            if self.container.status == 'exited':
                exitcode = self.container.attrs["State"]["ExitCode"]
                logs = self.container.logs()
                msg = f'Failed to start Docker container with image {image}, Container log: {logs}'
                raise DeadDockerContainerException(msg, exitcode, logs)

        super(BmiClientDocker, self).__init__(BmiClient.create_grpc_channel(port=port, host=host), timeout=timeout)

    def __del__(self):
        if hasattr(self, "container"):
            self.container.stop()

    def initialize(self, filename):
        fn = stage_config_file(filename, self.input_dir, self.input_mount_point)
        super(BmiClientDocker, self).initialize(fn)

    def get_value_ref(self, var_name):
        raise NotImplementedError("Cannot exchange memory references across process boundary")
