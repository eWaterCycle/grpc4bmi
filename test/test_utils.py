import pytest

from grpc4bmi.utils import stage_config_file


class TestStageConfigFile:
    def test_inside_inputdir(self, tmpdir):
        input_dir = tmpdir.mkdir('input')
        c = input_dir.join('config.cfg')
        c.write("something")

        result = stage_config_file(c, input_dir, input_mount_point='/data/input')
        assert result == '/data/input/config.cfg'

    def test_outside_inputdir(self, tmpdir):
        input_dir = tmpdir.mkdir('input')
        c = tmpdir.join('config.cfg')
        c.write("something")

        result = stage_config_file(c, input_dir, input_mount_point='/data/input')
        assert result == '/data/input/config.cfg'

    def test_outside_inputdir_beforeconfig(self, tmpdir):
        input_dir = tmpdir.mkdir('ainput')
        c = tmpdir.join('config.cfg')
        c.write("something")

        result = stage_config_file(c, input_dir, input_mount_point='/data/input')
        assert result == '/data/input/config.cfg'

    def test_cfg_in_container(self, tmpdir):
        input_dir = tmpdir.mkdir('input')

        c = '/somewhere/config.cfg'
        result = stage_config_file(c, input_dir, input_mount_point='/data/input')
        assert result == c

    def test_noinputdir(self, tmpdir):
        c = tmpdir.join('config.cfg')
        c.write("something")

        with pytest.raises(Exception) as exc_info:
            stage_config_file(c, None, None)
        assert str(exc_info.value).startswith('Unable to copy')
