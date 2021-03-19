from textwrap import dedent

import pytest
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat.v4 import new_notebook, new_code_cell

from grpc4bmi.bmi_client_singularity import BmiClientSingularity
from test.conftest import write_config, write_datafile

IMAGE_NAME = "docker://ewatercycle/walrus-grpc4bmi:v0.2.0"


@pytest.fixture()
def walrus_model(tmp_path, walrus_input):
    model = BmiClientSingularity(image=IMAGE_NAME, work_dir=str(tmp_path))
    yield model
    del model


@pytest.fixture()
def walrus_model_with_2input_dirs(walrus_2input_dirs):
    input_dirs = walrus_2input_dirs['input_dirs']
    model = BmiClientSingularity(image=IMAGE_NAME, input_dirs=input_dirs)
    yield model
    del model


@pytest.fixture()
def walrus_model_with_work_dir(tmp_path):
    work_dir = tmp_path
    write_config(work_dir / 'config.yml', 'PEQ_Hupsel.dat')
    write_datafile(work_dir / 'PEQ_Hupsel.dat')

    model = BmiClientSingularity(image=IMAGE_NAME, work_dir=str(work_dir))
    yield model, work_dir
    del model


class TestBmiClientSingularity:
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

    def test_2input_dirs(self, walrus_2input_dirs, walrus_model_with_2input_dirs):
        config_file = walrus_2input_dirs['cfg']
        walrus_model_with_2input_dirs.initialize(config_file)
        walrus_model_with_2input_dirs.update()

        # After initialization and update the forcings have been read from the extra volume
        assert len(walrus_model_with_2input_dirs.get_value('Q')) == 1

    def test_workdir_absolute(self, walrus_model_with_work_dir):
        model, work_dir = walrus_model_with_work_dir
        model.initialize(str(work_dir / 'config.yml'))
        model.update()

        # After initialization and update the forcings have been read from the work dir
        assert len(model.get_value('Q')) == 1

    def test_workdir_relative(self, walrus_model_with_work_dir):
        model, _work_dir = walrus_model_with_work_dir
        model.initialize('config.yml')
        model.update()

        # After initialization and update the forcings have been read from the work dir
        assert len(model.get_value('Q')) == 1

    def test_inputdir_absent(self, tmp_path):
        dirthatdoesnotexist = 'dirthatdoesnotexist'
        input_dir = tmp_path / dirthatdoesnotexist
        with pytest.raises(NotADirectoryError, match=dirthatdoesnotexist):
            BmiClientSingularity(image=IMAGE_NAME, input_dirs=[str(input_dir)])

    def test_workdir_absent(self, tmp_path):
        dirthatdoesnotexist = 'dirthatdoesnotexist'
        work_dir = tmp_path / dirthatdoesnotexist
        with pytest.raises(NotADirectoryError, match=dirthatdoesnotexist):
            BmiClientSingularity(image=IMAGE_NAME, work_dir=str(work_dir))

    def test_same_inputdir_and_workdir(self, tmp_path):
        some_dir = str(tmp_path)
        match = 'Found work_dir equal to one of the input directories. Please drop that input dir.'
        with pytest.raises(ValueError, match=match):
            BmiClientSingularity(image=IMAGE_NAME, input_dirs=(some_dir,), work_dir=some_dir)


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
