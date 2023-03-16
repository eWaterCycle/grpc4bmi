from io import BytesIO

import docker
import numpy as np
import pytest
from typeguard import TypeCheckError

from grpc4bmi.bmi_client_docker import BmiClientDocker
from grpc4bmi.exceptions import DeadContainerException
from grpc4bmi.reserve import reserve_grid_padding

walrus_docker_image = 'ewatercycle/walrus-grpc4bmi:v0.3.1'


@pytest.fixture()
def walrus_model(tmp_path, walrus_input):
    model = BmiClientDocker(image=walrus_docker_image, image_port=55555, work_dir=str(tmp_path))
    yield model
    del model


@pytest.fixture()
def exit_container():
    client = docker.from_env()
    prog = "import sys;print('my stderr log message', file=sys.stderr);print('my stdout log message');sys.exit(25)"
    dockerfile = BytesIO(f'FROM {walrus_docker_image}\nCMD ["python3", "-c", "{prog}" ]\n'.encode())
    image, logs = client.images.build(fileobj=dockerfile)
    yield image.id
    client.images.remove(image.id, force=True)


@pytest.fixture()
def walrus_model_with_2input_dirs(tmp_path, walrus_2input_dirs):
    input_dirs = walrus_2input_dirs['input_dirs']
    work_dir = tmp_path / 'work'
    work_dir.mkdir()
    model = BmiClientDocker(image="ewatercycle/walrus-grpc4bmi:v0.2.0",
                            image_port=55555,
                            work_dir=str(work_dir),
                            input_dirs=input_dirs)
    yield model
    del model


class TestBmiClientDocker:
    def test_component_name(self, walrus_model):
        assert walrus_model.get_component_name() == 'WALRUS'

    def test_get_grid_origin(self, walrus_input, walrus_model):
        walrus_model.initialize(str(walrus_input))
        grid_id = walrus_model.get_var_grid('Q')

        result = reserve_grid_padding(walrus_model, grid_id)
        assert len(walrus_model.get_grid_origin(grid_id, result)) == 2

    def test_initialize(self, walrus_input, walrus_model):
        walrus_model.initialize(str(walrus_input))
        assert walrus_model.get_current_time() == walrus_model.get_start_time()

    def test_get_value_ptr(self, walrus_model):
        with pytest.raises(NotImplementedError):
            walrus_model.get_value_ptr('Q')

    def test_get_var_location(self, walrus_model):
        assert walrus_model.get_var_location('Q') == 'node'

    def test_2input_dirs(self, walrus_2input_dirs, walrus_model_with_2input_dirs):
        config_file = walrus_2input_dirs['cfg']
        walrus_model_with_2input_dirs.initialize(config_file)
        walrus_model_with_2input_dirs.update()
        # After initialization and update the forcings have been read from the extra volume
        val = walrus_model_with_2input_dirs.get_value('Q', np.zeros((1,)))
        assert len(val) == 1

    def test_inputdir_absent(self, tmp_path):
        dirthatdoesnotexist = 'dirthatdoesnotexist'
        input_dir = tmp_path / dirthatdoesnotexist
        work_dir = tmp_path / 'work'
        work_dir.mkdir()
        with pytest.raises(NotADirectoryError, match=dirthatdoesnotexist):
            BmiClientDocker(image=walrus_docker_image, image_port=55555,
                            work_dir=str(work_dir), input_dirs=[str(input_dir)])

    def test_workdir_absent(self, tmp_path):
        dirthatdoesnotexist = 'dirthatdoesnotexist'
        work_dir = tmp_path / dirthatdoesnotexist
        with pytest.raises(NotADirectoryError, match=dirthatdoesnotexist):
            BmiClientDocker(image=walrus_docker_image, image_port=55555, work_dir=str(work_dir))

    def test_container_start_failure(self, exit_container, tmp_path):
        expected = r"Failed to start Docker container with image"
        with pytest.raises(DeadContainerException, match=expected) as excinfo:
            BmiClientDocker(image=exit_container, work_dir=str(tmp_path))

        assert excinfo.value.exitcode == 25
        assert 'my stderr' in excinfo.value.logs
        assert 'my stdout' in excinfo.value.logs

    def test_same_inputdir_and_workdir(self, tmp_path):
        some_dir = str(tmp_path)
        match = 'Found work_dir equal to one of the input directories. Please drop that input dir.'
        with pytest.raises(ValueError, match=match):
            BmiClientDocker(image=walrus_docker_image, image_port=55555, input_dirs=(some_dir,), work_dir=some_dir)

    def test_workdir_as_number(self):
        with pytest.raises(TypeCheckError, match='is not an instance of str'):
            BmiClientDocker(image=walrus_docker_image, work_dir=42)

    def test_inputdirs_as_str(self, tmp_path):
        some_dir = str(tmp_path)
        with pytest.raises(TypeError, match='must be collections.abc.Iterable'):
            BmiClientDocker(image=walrus_docker_image, input_dirs='old type', work_dir=some_dir)

    def test_inputdirs_as_number(self, tmp_path):
        some_dir = str(tmp_path)
        with pytest.raises(TypeCheckError, match='is not an instance of collections.abc.Iterable'):
            BmiClientDocker(image=walrus_docker_image, input_dirs=42, work_dir=some_dir)

    def test_logs(self, walrus_model, capfd):
        logs = walrus_model.logs()

        assert 'R[write to console]' in logs
        assert 'R[write to console]' not in capfd.readouterr().out
