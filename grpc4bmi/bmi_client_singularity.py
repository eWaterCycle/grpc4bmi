import errno
import os
from os.path import abspath
import subprocess
import sys
import logging

from semver import VersionInfo

from grpc4bmi.bmi_grpc_client import BmiClient
from grpc4bmi.utils import stage_config_file

REQUIRED_SINGULARITY_VERSION = '>=3.1.0'


def check_singularity_version():
    p = subprocess.Popen(['singularity', 'version'], stdout=subprocess.PIPE)
    (stdout, _stderr) = p.communicate()
    if p.returncode != 0:
        raise Exception('Unable to determine singularity version')
    if not VersionInfo.parse(stdout.decode('utf-8')).match(REQUIRED_SINGULARITY_VERSION):
        raise Exception(f'Wrong version of singularity found, require version {REQUIRED_SINGULARITY_VERSION}')
    return True


class BmiClientSingularity(BmiClient):
    """BMI GRPC client for singularity server processes
    During initialization launches a singularity container with run-bmi-server as its command.
    The client picks a random port and expects the container to run the server on that port.
    The port is passed to the container using the BMI_PORT environment variable.

    >>> from grpc4bmi.bmi_client_singularity import BmiClientSingularity
    >>> image = 'docker://ewatercycle/wflow-grpc4bmi:latest'
    >>> client = BmiClientSingularity(image, input_dir='wflow_rhine_sbm', output_dir='wflow_output')
    >>> client.initialize('wflow_rhine_sbm/wflow_sbm.ini')
    >>> client.update_until(client.get_end_time())
    >>> del client

    Args:
        image: Singularity image. For Docker Hub image use `docker://*`.
        input_dir (str): Directory for input files of model
        output_dir (str): Directory for input files of model
        timeout (int): Seconds to wait for gRPC client to connect to server
        extra_volumes (Dict[str,str]): Extra volumes to attach to Singularity container.

            The key is the hosts path and the value the mounted volume inside the container.
            Contrary to Docker client, extra volumes are always read/write

            For example:

            .. code-block:: python

                    {'/data/shared/forcings/': '/data/forcings'}

    """
    INPUT_MOUNT_POINT = "/data/input"
    OUTPUT_MOUNT_POINT = "/data/output"

    def __init__(self, image, input_dir=None, output_dir=None, timeout=None, extra_volumes=None):
        check_singularity_version()
        host = 'localhost'
        port = BmiClient.get_unique_port(host)
        args = [
            "singularity",
            "run",
        ]
        mount_points = {} if extra_volumes is None else extra_volumes
        if input_dir is not None:
            mount_points[input_dir] = BmiClientSingularity.INPUT_MOUNT_POINT
            self.input_dir = abspath(input_dir)
        if any(mount_points):
            args += ["--bind", ','.join([hp + ':' + ip for hp, ip in mount_points.items()])]
        if output_dir is not None:
            self.output_dir = abspath(output_dir)
            try:
                # Create output dir ourselves or singularity will complain
                os.mkdir(self.output_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise e
            args += ["--bind", output_dir + ':' + BmiClientSingularity.OUTPUT_MOUNT_POINT]
        args.append(image)
        env = os.environ.copy()
        env['BMI_PORT'] = str(port)
        logging.info(f'Running {image} singularity container on port {port}')
        self.container = subprocess.Popen(args, env=env, preexec_fn=os.setsid)
        super(BmiClientSingularity, self).__init__(BmiClient.create_grpc_channel(port=port, host=host), timeout=timeout)

    def __del__(self):
        if hasattr(self, "container"):
            self.container.terminate()
            self.container.wait()

    def initialize(self, filename):
        fn = stage_config_file(filename, self.input_dir, self.INPUT_MOUNT_POINT, home_mounted=True)
        super(BmiClientSingularity, self).initialize(fn)

    def get_value_ptr(self, var_name):
        raise NotImplementedError("Cannot exchange memory references across process boundary")
