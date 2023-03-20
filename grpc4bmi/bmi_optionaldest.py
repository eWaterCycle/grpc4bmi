from typing import Optional, Tuple
from bmipy import Bmi
import numpy as np

from grpc4bmi.reserve import reserve_grid_edge_nodes, reserve_grid_face_, reserve_grid_nodes, reserve_grid_padding, reserve_grid_shape, reserve_grid_nodes_per_face, reserve_values, reserve_values_at_indices

class OptionalDestBmi(Bmi):
    """Proxy around Bmi object that makes the output argument (dest) optional.

    Some Bmi methods accept a numpy array as argument (dest) that must be filled by the model.
    This class makes that argument optional.

    For example to get the value of a `heat model <https://github.com/csdms/bmi-example-python>`_:

    .. code-block:: python

            from heat import BmiHeat
            import numpy as np

            orig_model = BmiHeat()
            orig_model.initialize()
            dest = np.empty((200,), dtype=np.float64)
            dest2 = orig_model.get_value('plate_surface__temperature', dest)
            

    A `dest` variable must created and passed to the `get_value` method.
    It must be set to a Numpy array with the shape and type the model requires.
    The returned numpy array (`dest2`) is the same as the `dest` numpy array.
    By using this class we no longer need do create and pass it.

    .. code-block:: python

        from grpc4bmi.bmi_optionaldest import OptionalDestBmi

        model = OptionalDestBmi(orig_model)
        dest3 = model.get_value('plate_surface__temperature')

    This class will create dest variables by calling other Bmi methods for its shape.
    When using a slow model it is strongly suggested to wrap the BmiClient with :class:`grpc4bmi.bmi_memoized.MemoizedBmi` first to prevent a lot of calls.

    The `dest` in :external+bmipy:ref:`bmipy.Bmi.get_value_at_indices(self, name, dest, inds) <get_value_at_indices>` method
    can not be made optional so it has been changed to
    :func:`OptionalDestBmi.get_value_at_indices(self, name, inds) <grpc4bmi.bmi_optionaldest.OptionalDestBmi.get_value_at_indices>`.
    """
    def __init__(self, origin: Bmi):
        self.origin = origin

    def initialize(self, config_file: Optional[str]) -> None:
        return self.origin.initialize(config_file)

    def update(self) -> None:
        self.origin.update()

    def update_until(self, time) -> None:
        self.origin.update_until(time)

    def finalize(self) -> None:
        self.origin.finalize()

    def get_component_name(self) -> str:
        return self.origin.get_component_name()

    def get_input_item_count(self) -> int:
        return self.origin.get_input_item_count()

    def get_output_item_count(self) -> int:
        return self.origin.get_output_item_count()

    def get_input_var_names(self) -> Tuple[str]:
        return self.origin.get_input_var_names()

    def get_output_var_names(self) -> Tuple[str]:
        return self.origin.get_output_var_names()

    def get_start_time(self) -> float:
        return self.origin.get_start_time()

    def get_current_time(self) -> float:
        return self.origin.get_current_time()

    def get_end_time(self) -> float:
        return self.origin.get_end_time()

    def get_time_step(self) -> float:
        return self.origin.get_time_step()

    def get_time_units(self) -> str:
        return self.origin.get_time_units()

    def get_var_type(self, name: str) -> str:
        return self.origin.get_var_type(name)

    def get_var_units(self, name: str) -> str:
        return self.origin.get_var_units(name)

    def get_var_itemsize(self, name: str) -> int:
        return self.origin.get_var_itemsize(name)

    def get_var_nbytes(self, name: str) -> int:
        return self.origin.get_var_nbytes(name)

    def get_var_location(self, name: str) -> str:
        return self.origin.get_var_location(name)

    def get_var_grid(self, name: str) -> int:
        return self.origin.get_var_grid(name)

    def get_value(self, name, dest: Optional[np.ndarray]=None) -> np.ndarray:
        if dest is None:
            dest = reserve_values(self.origin, name)
        return self.origin.get_value(name, dest)

    def get_value_ptr(self, name: str) -> np.ndarray:
        return self.origin.get_value_ptr(name)  

    def get_value_at_indices(self, name: str, inds: np.ndarray) -> np.ndarray:
        """Get values at particular indices.

        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        inds : array_like
            The indices into the variable array.

        Returns
        -------
        array_like
            Value of the model variable at the given location.
        """
        dest = reserve_values_at_indices(self.origin, name, inds)
        return self.origin.get_value_at_indices(name, dest, inds)

    def set_value(self, name: str, values: np.ndarray) -> None:
        return self.origin.set_value(name, values)

    def set_value_at_indices(self, name: str, inds: np.ndarray, src: np.ndarray) -> None:
        return self.origin.set_value_at_indices(name, inds, src)

    def get_grid_shape(self, grid: int, shape: Optional[np.ndarray]=None) -> np.ndarray:
        if shape is None:
            shape = reserve_grid_shape(self.origin, grid)
        return self.origin.get_grid_shape(grid, shape)

    def get_grid_x(self, grid: int, x: Optional[np.ndarray]=None) -> np.ndarray:
        if x is None:
            x = reserve_grid_nodes(self.origin, grid, 0)
        return self.origin.get_grid_x(grid, x)

    def get_grid_y(self, grid: int, y: Optional[np.ndarray]=None) -> np.ndarray:
        if y is None:
            y = reserve_grid_nodes(self.origin, grid, 1)
        return self.origin.get_grid_y(grid, y)

    def get_grid_z(self, grid: int, z: Optional[np.ndarray]=None) -> np.ndarray:
        if z is None:
            z = reserve_grid_nodes(self.origin, grid, 2)
        return self.origin.get_grid_z(grid, z)

    def get_grid_spacing(self, grid: int, spacing: Optional[np.ndarray]=None) -> np.ndarray:
        if spacing is None:
            spacing = reserve_grid_padding(self.origin, grid)
        return self.origin.get_grid_spacing(grid, spacing)

    def get_grid_origin(self, grid: int, origin: Optional[np.ndarray]=None) -> np.ndarray:
        if origin is None:
            origin = reserve_grid_padding(self.origin, grid)
        return self.origin.get_grid_origin(grid, origin)

    def get_grid_rank(self, grid: int) -> int:
        return self.origin.get_grid_rank(grid)

    def get_grid_size(self, grid: int) -> int:
        return self.origin.get_grid_size(grid)

    def get_grid_type(self, grid: int) -> str:
        return self.origin.get_grid_type(grid)

    def get_grid_node_count(self, grid: int) -> int:
        return self.origin.get_grid_node_count(grid)

    def get_grid_edge_count(self, grid: int) -> int:
        return self.origin.get_grid_edge_count(grid)

    def get_grid_face_count(self, grid: int) -> int:
        return self.origin.get_grid_face_count(grid)

    def get_grid_edge_nodes(self, grid: int, edge_nodes: Optional[np.ndarray]=None) -> np.ndarray:
        if edge_nodes is None:
            edge_nodes = reserve_grid_edge_nodes(self.origin, grid)
        return self.origin.get_grid_edge_nodes(grid, edge_nodes)

    def get_grid_face_edges(self, grid: int, face_edges: Optional[np.ndarray]=None) -> np.ndarray:
        if face_edges is None:
            face_edges = reserve_grid_face_(self.origin, grid)
        return self.origin.get_grid_face_edges(grid, face_edges)

    def get_grid_face_nodes(self, grid: int, face_nodes: Optional[np.ndarray]=None) -> np.ndarray:
        if face_nodes is None:
            face_nodes = reserve_grid_face_(self.origin, grid)
        return self.origin.get_grid_face_nodes(grid, face_nodes)
    
    def get_grid_nodes_per_face(self, grid: int, nodes_per_face: Optional[np.ndarray]=None) -> np.ndarray:
        if nodes_per_face is None:
            nodes_per_face = reserve_grid_nodes_per_face(self.origin, grid)
        return self.origin.get_grid_nodes_per_face(grid, nodes_per_face)
