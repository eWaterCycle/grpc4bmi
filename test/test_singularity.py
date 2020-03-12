from textwrap import dedent

from os import environ
import pytest
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat.v4 import new_notebook, new_code_cell

from grpc4bmi.bmi_client_singularity import BmiClientSingularity
from grpc4bmi.reserve import reserve_grid_padding

IMAGE_NAME = "docker://ewatercycle/walrus-grpc4bmi:v0.3.1"


@pytest.fixture()
def walrus_model(tmp_path, walrus_input):
    model = BmiClientSingularity(image=IMAGE_NAME, input_dir=str(tmp_path))
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

    def test_get_grid_origin(self, walrus_input, walrus_model):
        walrus_model.initialize(str(walrus_input))
        grid_id = walrus_model.get_var_grid('Q')
        assert len(walrus_model.get_grid_origin(grid_id, reserve_grid_padding(walrus_model, grid_id))) == 2


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


@pytest.mark.skipif(environ.get('TRAVIS', False), reason="Does not work on Travis-CI")
def test_from_notebook(notebook, tmp_path):
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(notebook, {'metadata': {'path': tmp_path}})
