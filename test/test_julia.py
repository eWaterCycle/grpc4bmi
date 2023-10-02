from pathlib import Path
from textwrap import dedent
import numpy as np
import pytest

try:
    from grpc4bmi.bmi_julia_model import install, BmiJulia
    from juliacall import Main as jl
except ImportError:
    BmiJulia = None


@pytest.mark.skipif(not BmiJulia, reason="R and its dependencies are not installed")
@pytest.fixture(scope="module")
def install_heat():
    jl.Pkg.add(
        url="https://github.com/csdms/bmi-example-julia.git",
        rev="d8b354ceddf6b048727c2e214031f43d62964120",
    )


@pytest.mark.skipif(not BmiJulia, reason="R and its dependencies are not installed")
class TestFakeFailingModel:
    @pytest.fixture
    def cfg_file(self, tmp_path: Path):
        fn = tmp_path / "heat.toml"
        fn.write_text(
            dedent(
                """\
            # Heat model configuration
            shape = [6, 8]
            spacing = [1.0, 1.0]
            origin = [0.0, 0.0]
            alpha = 1.0
        """
            )
        )
        return fn

    @pytest.fixture
    def model(self, cfg_file):
        model = BmiJulia("Heat.Model")
        model.initialize(str(cfg_file))
        return model

    @pytest.mark.parametrize(
        "fn_name,fn_args,expected",
        [
            ("get_component_name", tuple(), "The 2D Heat Equation"),
            ('get_input_item_count', tuple(), 1),
            ('get_output_item_count', tuple(), 1),
            ('get_input_var_names', tuple(), ['plate_surface__temperature']),
            ('get_output_var_names', tuple(), ['plate_surface__temperature']),
            ('get_start_time', tuple(), 0.0),
            ('get_end_time', tuple(), np.Inf),
            ('get_time_step', tuple(), 0.25),
            ('get_time_units', tuple(), 's'),
        ],
    )
    def test_methods(self, model: BmiJulia, fn_name, fn_args, expected):
        fn = getattr(model, fn_name)
        if fn_args == tuple():
            result = fn()
        else:
            result = fn(*fn_args)
        # TODO almost equal
        assert result == expected
