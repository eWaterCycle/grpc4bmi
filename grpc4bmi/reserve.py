"""Helpers to reserve numpy arrays for use in some of the Bmi methods as output argument
"""
import numpy

from bmipy import Bmi


def reserve_values(model: Bmi, name: str) -> numpy.ndarray:
    """Reserve dest for :func:`bmipy.Bmi.get_value`"""
    dtype = model.get_var_type(name)
    item_size = model.get_var_itemsize(name)
    total_size = model.get_var_nbytes(name)
    size = total_size // item_size
    return numpy.empty(size, dtype=dtype)


def reserve_grid_shape(model: Bmi, grid_id: int) -> numpy.ndarray:
    """Reserve shape for :func:`bmipy.Bmi.get_grid_shape`"""
    return numpy.empty(model.get_grid_rank(grid_id), dtype=numpy.int64)


def reserve_grid_padding(model: Bmi, grid_id: int) -> numpy.ndarray:
    """Reserve dest for :func:`bmipy.Bmi.get_grid_spacing` and :func:`bmipy.Bmi.get_grid_origin`
    """
    return numpy.empty(model.get_grid_rank(grid_id), dtype=numpy.float64)


def reserve_grid_nodes(model: Bmi, grid_id: int, dim_index: int) -> numpy.ndarray:
    """Reserve dest for :func:`bmipy.Bmi.get_grid_x`, :func:`bmipy.Bmi.get_grid_y` and :func:`bmipy.Bmi.get_grid_z`

    The dim_index goes x,y,z and model.get_grid_shape goes z,y,x or y,x so index is inverted
    """
    model_type = model.get_grid_type(grid_id)
    if model_type in {'uniform_rectilinear', 'rectilinear'}:
        grid_shape = model.get_grid_shape(grid_id, reserve_grid_shape(model, grid_id))
        shape = grid_shape[::-1][dim_index]
    else:
        shape = model.get_grid_size(grid_id)
    return numpy.empty(shape, dtype=numpy.float64)


def reserve_values_at_indices(model: Bmi, name: str, indices) -> numpy.ndarray:
    """Reserve dest for :func:`bmipy.Bmi.get_value_at_indices` """
    dtype = model.get_var_type(name)
    return numpy.empty(len(indices), dtype=dtype)
