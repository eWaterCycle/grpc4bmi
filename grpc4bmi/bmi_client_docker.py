import docker

from grpc4bmi.bmi_grpc_client import BmiClient


class BmiClientDocker(BmiClient):

    def __init__(self, image, module=None):
        client = docker.from_env()
        port = BmiClient.get_unique_port()
        # internal_port = BmiClient.start_port
        # args = ["run-bmi-server", "--port", str(internal_port)]
        # if module is not None:
        #     args.extend(["--name", module])
        # ports = {'/'.join([str(internal_port), "tcp"]): port}

        self.container = client.containers.run(image, ports={"50051/tcp": port}, detach=True)
        super(BmiClientDocker, self).__init__(BmiClient.create_grpc_channel(port=port))

    def __del__(self):
        self.container.stop()

    def get_value_ref(self, var_name):
        raise NotImplementedError("Cannot exchange memory references across process boundary")
