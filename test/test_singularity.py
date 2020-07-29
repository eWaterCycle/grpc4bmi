from textwrap import dedent

import pytest
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat.v4 import new_notebook, new_code_cell

from grpc4bmi.bmi_client_singularity import BmiClientSingularity

IMAGE_NAME = "docker://ewatercycle/walrus-grpc4bmi:v0.2.0"


@pytest.fixture()
def walrus_model(tmp_path, walrus_input):
    model = BmiClientSingularity(image=IMAGE_NAME, input_dir=str(tmp_path))
    yield model
    del model


@pytest.fixture()
def walrus_model_with_extra_volume(walrus_input_on_extra_volume):
    (input_dir, docker_extra_volumes) = walrus_input_on_extra_volume
    extra_volumes = {str(k): str(v['bind']) for k, v in docker_extra_volumes.items()}
    model = BmiClientSingularity(image=IMAGE_NAME, input_dir=str(input_dir), extra_volumes=extra_volumes)
    yield model
    del model


class TestBmiClientDocker:
    def test_component_name(self, walrus_model):
        assert walrus_model.get_component_name() == 'WALRUS'

    def test_initialize(self, walrus_input, walrus_model):
        walrus_model.initialize(str(walrus_input))
        assert walrus_model.get_current_time() == walrus_model.get_start_time()

    def test_get_value_ref(self, walrus_model):
        with pytest.raises(NotImplementedError):
            walrus_model.get_value_ref('Q')

    def test_get_grid_x(self, walrus_input, walrus_model):
        walrus_model.initialize(str(walrus_input))
        grid_id = walrus_model.get_var_grid('Q')
        assert len(walrus_model.get_grid_x(grid_id)) == 1

    def test_extra_volumes(self, walrus_model_with_extra_volume):
        walrus_model_with_extra_volume.initialize('/data/input/config.yml')
        walrus_model_with_extra_volume.update()

        # After initialization and update the forcings have been read from the extra volume
        assert len(walrus_model_with_extra_volume.get_value('Q')) == 1

@pytest.fixture
def notebook():
    cells = [
        new_code_cell(dedent("""\
            from grpc4bmi.bmi_client_singularity import BmiClientSingularity
            walrus_model = BmiClientSingularity(image='{0}')
            assert walrus_model.get_component_name() == 'WALRUS'
            del walrus_model
        """.format(IMAGE_NAME)))
    ]
    return new_notebook(cells=cells)


def test_from_notebook(notebook, tmp_path):
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(notebook, {'metadata': {'path': tmp_path}})
