import os
import subprocess
from tempfile import TemporaryDirectory
from textwrap import dedent
from typing import Type, Union

import pytest
from grpc import RpcError
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat.v4 import new_notebook, new_code_cell

from grpc4bmi.bmi_client_singularity import SUPPORTED_APPTAINER_VERSIONS, SUPPORTED_SINGULARITY_VERSIONS, BmiClientSingularity, check_singularity_version_string
from grpc4bmi.exceptions import ApptainerVersionException, DeadContainerException, SingularityVersionException
from test.conftest import write_config, write_datafile

IMAGE_NAME = "docker://ewatercycle/walrus-grpc4bmi:v0.2.0"


@pytest.fixture()
def walrus_model(tmp_path, walrus_input):
    model = BmiClientSingularity(image=IMAGE_NAME, work_dir=str(tmp_path))
    yield model
    del model


@pytest.fixture()
def walrus_model_with_input_dir(tmp_path, walrus_input):
    work_dir = TemporaryDirectory()
    model = BmiClientSingularity(image=IMAGE_NAME, work_dir=work_dir.name, input_dirs=[str(tmp_path)])
    yield model
    del model
    work_dir.cleanup()


@pytest.fixture()
def walrus_model_with_2input_dirs(walrus_2input_dirs, tmp_path):
    work_dir = tmp_path / 'work'
    work_dir.mkdir()
    input_dirs = walrus_2input_dirs['input_dirs']
    model = BmiClientSingularity(image=IMAGE_NAME, work_dir=str(work_dir), input_dirs=input_dirs)
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


@pytest.fixture()
def walrus_model_with_config_inside_image(tmp_path):
    input_dir = tmp_path / 'input'
    input_dir.mkdir()
    data_file = input_dir / 'PEQ_Hupsel.dat'
    write_datafile(data_file)
    cfg_file = input_dir / 'config.yml'
    write_config(cfg_file, '/scratch/PEQ_Hupsel.dat')
    def_file = tmp_path / 'walrus.def'
    def_file.write_text(f'''Bootstrap: docker
From: {IMAGE_NAME.replace('docker://', '')}

%files
  {data_file} /scratch/PEQ_Hupsel.dat'
  {cfg_file} /scratch/config.yml'
''')
    image = tmp_path / 'walrus-image'
    subprocess.run(['singularity', 'build', '--sandbox', '--fakeroot', image, def_file])

    work_dir = tmp_path / 'work'
    work_dir.mkdir()
    model = BmiClientSingularity(str(image), str(work_dir))

    yield model

    del model
    # Singularity generates some files with permissions that pytest clean up does not handle
    subprocess.run(['rm', '-rf', str(image)])


class TestBmiClientSingularity:
    def test_component_name(self, walrus_model):
        assert walrus_model.get_component_name() == 'WALRUS'

    def test_initialize(self, walrus_input, walrus_model):
        walrus_model.initialize(str(walrus_input))
        assert walrus_model.get_current_time() == walrus_model.get_start_time()

    def test_initialize_absent_configfile(self, walrus_model):
        with pytest.raises(RpcError, match='Exception calling application'):
            walrus_model.initialize('configfilethatdoesnotexist')

    def test_get_value_ref(self, walrus_model):
        with pytest.raises(NotImplementedError):
            walrus_model.get_value_ref('Q')

    def test_get_grid_x(self, walrus_input, walrus_model):
        walrus_model.initialize(str(walrus_input))
        grid_id = walrus_model.get_var_grid('Q')
        assert len(walrus_model.get_grid_x(grid_id)) == 1

    def test_input_dir(self, walrus_input, walrus_model_with_input_dir):
        walrus_model_with_input_dir.initialize(str(walrus_input))
        walrus_model_with_input_dir.update()

        # After initialization and update the forcings have been read from the forcing dir
        assert len(walrus_model_with_input_dir.get_value('Q')) == 1

    def test_2input_dirs(self, walrus_2input_dirs, walrus_model_with_2input_dirs):
        config_file = walrus_2input_dirs['cfg']
        walrus_model_with_2input_dirs.initialize(config_file)
        walrus_model_with_2input_dirs.update()

        # After initialization and update the forcings have been read from the forcing dir
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
        work_dir = tmp_path / 'work'
        work_dir.mkdir()
        with pytest.raises(NotADirectoryError, match=dirthatdoesnotexist):
            BmiClientSingularity(image=IMAGE_NAME, work_dir=str(work_dir), input_dirs=[str(input_dir)])

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

    def test_with_config_inside_image(self, walrus_model_with_config_inside_image):
        model = walrus_model_with_config_inside_image
        model.initialize('/scratch/config.yml')
        model.update()

        # After initialization and update the forcings have been read from the scratch dir
        assert len(model.get_value('Q')) == 1

    def test_workdir_as_number(self):
        with pytest.raises(TypeError, match='must be str'):
            BmiClientSingularity(image=IMAGE_NAME, work_dir=42)

    def test_inputdirs_as_str(self, tmp_path):
        some_dir = str(tmp_path)
        with pytest.raises(TypeError, match='must be collections.abc.Iterable; got str instead'):
            BmiClientSingularity(image=IMAGE_NAME, input_dirs='old type', work_dir=some_dir)

    def test_inputdirs_as_number(self, tmp_path):
        some_dir = str(tmp_path)
        with pytest.raises(TypeError, match='must be collections.abc.Iterable; got int instead'):
            BmiClientSingularity(image=IMAGE_NAME, input_dirs=42, work_dir=some_dir)


class TestRedirectOutput:
    EXPECTED = 'Hello from Docker!'

    @pytest.fixture
    def image(self):
        hello_image = 'docker://hello-world'
        # Cache image, first test does not use delay time to build image
        os.system(f'singularity run {hello_image}')
        return hello_image

    def test_default(self, image, tmp_path, capfd):
        with pytest.raises(DeadContainerException) as excinf:
            BmiClientSingularity(image=image, work_dir=str(tmp_path), delay=2)

        assert self.EXPECTED not in capfd.readouterr().out
        assert self.EXPECTED in excinf.value.logs

    def test_devnull(self, image, tmp_path, capfd):
        with pytest.raises(DeadContainerException) as excinf:
            BmiClientSingularity(image=image, work_dir=str(tmp_path), capture_logs=False, delay=2)

        assert self.EXPECTED not in capfd.readouterr().out
        assert self.EXPECTED not in excinf.value.logs


@pytest.fixture
def notebook(tmp_path):
    tmp_path.mkdir(exist_ok=True)
    cells = [
        new_code_cell(dedent("""\
            from grpc4bmi.bmi_client_singularity import BmiClientSingularity
            walrus_model = BmiClientSingularity(image='{0}', work_dir='{1}')
            assert walrus_model.get_component_name() == 'WALRUS'
            del walrus_model
        """.format(IMAGE_NAME, str(tmp_path))))
    ]
    return new_notebook(cells=cells)


def test_from_notebook(notebook, tmp_path):
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(notebook, {'metadata': {'path': tmp_path}})

class Test_check_singularity_version_string:
    @pytest.mark.parametrize("test_input", [
        ('singularity version 3.6.0'),
        ('singularity version 3.8.7'),  # Last OSS version before fork
        ('apptainer version 1.0.0-rc.2'),  
        ('apptainer version 1.0.0'),
        ('apptainer version 1.0.3'),
        ('apptainer version 1.1.0-rc.3'),
        ('apptainer version 1.1.2'),
    ])
    def test_ok(self, test_input: str):
        result = check_singularity_version_string(test_input)
        assert result


    @pytest.mark.parametrize("test_input,error_class,expected", [
        ('singularity version 3.5.0', SingularityVersionException, SUPPORTED_SINGULARITY_VERSIONS),
        ('apptainer version 1.0.0-rc.1', ApptainerVersionException, SUPPORTED_APPTAINER_VERSIONS),
        ('apptainer version 0.1.0', ApptainerVersionException, SUPPORTED_APPTAINER_VERSIONS),
    ])
    def test_too_old(self, test_input: str, error_class: Union[Type[ApptainerVersionException], Type[SingularityVersionException]], expected: str):
        with pytest.raises(error_class, match=expected):
            check_singularity_version_string(test_input)
