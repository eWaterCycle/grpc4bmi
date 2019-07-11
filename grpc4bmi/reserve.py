import numpy

from bmipy import Bmi


def reserve_values(model: Bmi, name: str) -> numpy.ndarray:
    dtype = model.get_var_type(name)
    item_size = model.get_var_itemsize(name)
    total_size = model.get_var_nbytes(name)
    size = total_size // item_size
    return numpy.empty(size, dtype=dtype)


def reserve_grid_values(model: Bmi, grid_id: int) -> numpy.ndarray:
    return numpy.empty(model.get_grid_rank(grid_id), dtype=numpy.int32)


def reserve_shape(model: Bmi, grid_id: int, dim_index: int):
    shape = model.get_grid_shape(grid_id, reserve_grid_values(model, grid_id))
    return numpy.empty(shape[dim_index], dtype=numpy.float64)
