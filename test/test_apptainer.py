import os
from typing import Type, Union

import pytest

from grpc4bmi.bmi_client_apptainer import SUPPORTED_APPTAINER_VERSIONS, BmiClientApptainer, check_apptainer_version_string
from grpc4bmi.exceptions import ApptainerVersionException, DeadContainerException

class Test_check_apptainer_version_string:
    @pytest.mark.parametrize("test_input", [
        ('apptainer version 1.0.0-rc.2'),  
        ('apptainer version 1.0.0'),
        ('apptainer version 1.0.3'),
        ('apptainer version 1.1.0-rc.3'),
        ('apptainer version 1.1.2'),
    ])
    def test_ok(self, test_input: str):
        result = check_apptainer_version_string(test_input)
        assert result

    @pytest.mark.parametrize("test_input,error_class,expected", [
        ('apptainer version 1.0.0-rc.1', ApptainerVersionException, SUPPORTED_APPTAINER_VERSIONS),
        ('apptainer version 0.1.0', ApptainerVersionException, SUPPORTED_APPTAINER_VERSIONS),
    ])
    def test_too_old(self, test_input: str, error_class: Type[ApptainerVersionException], expected: str):
        with pytest.raises(error_class, match=expected):
            check_apptainer_version_string(test_input)

IMAGE_NAME = "docker://ewatercycle/walrus-grpc4bmi:v0.2.0"

@pytest.fixture
def walrus_model(tmp_path, walrus_input):
    model = BmiClientApptainer(image=IMAGE_NAME, work_dir=str(tmp_path))
    yield model
    del model

class TestBmiClientApptainerHappyDays:
    def test_component_name(self, walrus_model):
        assert walrus_model.get_component_name() == 'WALRUS'

class TestBmiClientApptainerBadDays:
    def test_get_value_ref(self, walrus_model):
        with pytest.raises(NotImplementedError):
            walrus_model.get_value_ref('Q')

    def test_inputdir_absent(self, tmp_path):
        dirthatdoesnotexist = 'dirthatdoesnotexist'
        input_dir = tmp_path / dirthatdoesnotexist
        work_dir = tmp_path / 'work'
        work_dir.mkdir()
        with pytest.raises(NotADirectoryError, match=dirthatdoesnotexist):
            BmiClientApptainer(image=IMAGE_NAME, work_dir=str(work_dir), input_dirs=[str(input_dir)])

    def test_workdir_absent(self, tmp_path):
        dirthatdoesnotexist = 'dirthatdoesnotexist'
        work_dir = tmp_path / dirthatdoesnotexist
        with pytest.raises(NotADirectoryError, match=dirthatdoesnotexist):
            BmiClientApptainer(image=IMAGE_NAME, work_dir=str(work_dir))

    def test_same_inputdir_and_workdir(self, tmp_path):
        some_dir = str(tmp_path)
        match = 'Found work_dir equal to one of the input directories. Please drop that input dir.'
        with pytest.raises(ValueError, match=match):
            BmiClientApptainer(image=IMAGE_NAME, input_dirs=(some_dir,), work_dir=some_dir)

    def test_workdir_as_number(self):
        with pytest.raises(TypeError, match='must be str'):
            BmiClientApptainer(image=IMAGE_NAME, work_dir=42)

    def test_inputdirs_as_str(self, tmp_path):
        some_dir = str(tmp_path)
        with pytest.raises(TypeError, match='must be collections.abc.Iterable; got str instead'):
            BmiClientApptainer(image=IMAGE_NAME, input_dirs='old type', work_dir=some_dir)

    def test_inputdirs_as_number(self, tmp_path):
        some_dir = str(tmp_path)
        with pytest.raises(TypeError, match='must be collections.abc.Iterable; got int instead'):
            BmiClientApptainer(image=IMAGE_NAME, input_dirs=42, work_dir=some_dir)



class TestRedirectOutput:
    EXPECTED = 'Hello from Docker!'

    @pytest.fixture(scope="module")
    def image(self):
        hello_image = 'docker://hello-world'
        # Cache image, first test does not use delay time to build image
        os.system(f'apptainer run {hello_image}')
        return hello_image

    def test_default(self, image, tmp_path, capfd):
        with pytest.raises(DeadContainerException) as excinf:
            BmiClientApptainer(image=image, work_dir=str(tmp_path), delay=2)

        assert self.EXPECTED not in capfd.readouterr().out
        assert self.EXPECTED in excinf.value.logs

    def test_devnull(self, image, tmp_path, capfd):
        with pytest.raises(DeadContainerException) as excinf:
            BmiClientApptainer(image=image, work_dir=str(tmp_path), capture_logs=False, delay=2)

        assert self.EXPECTED not in capfd.readouterr().out
        assert self.EXPECTED not in excinf.value.logs
