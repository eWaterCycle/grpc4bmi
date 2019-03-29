import errno
import os
from os.path import abspath
import subprocess
import sys
import logging

import semver

from grpc4bmi.bmi_grpc_client import BmiClient
from grpc4bmi.utils import stage_config_file

REQUIRED_SINGULARITY_VERSION = '>=3.1.0'


def check_singularity_version():
    p = subprocess.Popen(['singularity', 'version'], stdout=subprocess.PIPE)
    (stdout, _stderr) = p.communicate()
    if p.returncode != 0:
        raise Exception('Unable to determine singularity version')
    if not semver.match(stdout.decode('utf-8'), REQUIRED_SINGULARITY_VERSION):
        raise Exception(f'Wrong version of singularity found, require version {REQUIRED_SINGULARITY_VERSION}')
    return True


class BmiClientSingularity(BmiClient):
    """BMI GRPC client for singularity server processes
    During initialization launches a singularity container with run-bmi-server as its command.
    The container exposes a port the client connects to.

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

    """
    INPUT_MOUNT_POINT = "/data/input"
    OUTPUT_MOUNT_POINT = "/data/output"

    def __init__(self, image, input_dir=None, output_dir=None):
        check_singularity_version()
        host = 'localhost'
        port = BmiClient.get_unique_port(host)
        args = [
            "singularity",
            "run",
        ]
        if input_dir is not None:
            self.input_dir = abspath(input_dir)
            args += ["--bind", input_dir + ':' + BmiClientSingularity.INPUT_MOUNT_POINT]
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
        self.container = subprocess.Popen(args, stderr=sys.stderr, stdout=sys.stdout, env=env, preexec_fn=os.setsid)
        super(BmiClientSingularity, self).__init__(BmiClient.create_grpc_channel(port=port, host=host))

    def __del__(self):
        if hasattr(self, "container"):
            self.container.terminate()
            self.container.wait()

    def initialize(self, filename):
        fn = stage_config_file(filename, self.input_dir, self.INPUT_MOUNT_POINT, home_mounted=True)
        super(BmiClientSingularity, self).initialize(fn)

    def get_value_ref(self, var_name):
        raise NotImplementedError("Cannot exchange memory references across process boundary")
