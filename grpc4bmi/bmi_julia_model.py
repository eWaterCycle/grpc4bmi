from typing import List

from bmipy import Bmi
import numpy as np
from juliacall import Main as jl

def install(package):
    """Add package to Julia environment.
    
    Args:
        package: Name of package to install.
    """
    jl.Pkg.add(package)

class BmiJulia(Bmi):
    """Python Wrapper of a Julia based implementation of BasicModelInterface.

    BasicModelInterface is available in https://github.com/Deltares/BasicModelInterface.jl repo.

    Args:
        model_name: Name of Julia model class 
        implementation_name: Name of Julia variable which implements BasicModelInterface

    """
    state = None

    def __init__(self, model_name, implementation_name = 'BasicModelInterface'):
        package4model = model_name.split('.')[0]
        package4implementation = implementation_name.split('.')[0]
        jl.seval("import " + package4model)
        jl.seval("import " + package4implementation)
        self.model = jl.seval(model_name)
        self.implementation = jl.seval(implementation_name)

    def initialize(self, config_file: str) -> None:
        """Perform startup tasks for the model.
        Perform all tasks that take place before entering the model's time
        loop, including opening files and initializing the model state. Model
        inputs are read from a text-based configuration file, specified by
        `config_file`.
        Parameters
        ----------
        config_file : str, optional
            The path to the model configuration file.
        Notes
        -----
        Models should be refactored, if necessary, to use a
        configuration file. CSDMS does not impose any constraint on
        how configuration files are formatted, although YAML is
        recommended. A template of a model's configuration file
        with placeholder values is used by the BMI.
        """
        self.state = self.implementation.initialize(self.model, config_file)

    def update(self) -> None:
        """Advance model state by one time step.
        Perform all tasks that take place within one pass through the model's
        time loop. This typically includes incrementing all of the model's
        state variables. If the model's state variables don't change in time,
        then they can be computed by the :func:`initialize` method and this
        method can return with no action.
        """
        self.implementation.update(self.state)

    def update_until(self, time: float) -> None:
        """Advance model state until the given time.
        Parameters
        ----------
        time : float
            A model time later than the current model time.
        """
        self.implementation.update_until(self.state, time)

    def finalize(self) -> None:
        """Perform tear-down tasks for the model.
        Perform all tasks that take place after exiting the model's time
        loop. This typically includes deallocating memory, closing files and
        printing reports.
        """
        self.implementation.finalize(self.state)

    def get_component_name(self) -> str:
        """Name of the component.
        Returns
        -------
        str
            The name of the component.
        """
        return self.implementation.get_component_name(self.state)

    def get_input_item_count(self) -> int:
        """Count of a model's input variables.
        Returns
        -------
        int
          The number of input variables.
        """
        return self.implementation.get_input_item_count(self.state)

    def get_output_item_count(self) -> int:
        """Count of a model's output variables.
        Returns
        -------
        int
          The number of output variables.
        """
        return self.implementation.get_output_item_count(self.state)

    def get_input_var_names(self) -> List[str]:
        """List of a model's input variables.
        Input variable names must be CSDMS Standard Names, also known
        as *long variable names*.
        Returns
        -------
        list of str
            The input variables for the model.
        Notes
        -----
        Standard Names enable the CSDMS framework to determine whether
        an input variable in one model is equivalent to, or compatible
        with, an output variable in another model. This allows the
        framework to automatically connect components.
        Standard Names do not have to be used within the model.
        """
        return list(self.implementation.get_input_var_names(self.state))

    def get_output_var_names(self) -> List[str]:
        """List of a model's output variables.
        Output variable names must be CSDMS Standard Names, also known
        as *long variable names*.
        Returns
        -------
        list of str
            The output variables for the model.
        """
        return list(self.implementation.get_output_var_names(self.state))

    def get_var_grid(self, name: str) -> int:
        """Get grid identifier for the given variable.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        Returns
        -------
        int
          The grid identifier.
        """
        return self.implementation.get_var_grid(self.state, name)

    def get_var_type(self, name: str) -> str:
        """Get data type of the given variable.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        Returns
        -------
        str
            The Python variable type; e.g., ``str``, ``int``, ``float``.
        """
        return self.implementation.get_var_type(self.state, name)

    def get_var_units(self, name: str) -> str:
        """Get units of the given variable.
        Standard unit names, in lower case, should be used, such as
        ``meters`` or ``seconds``. Standard abbreviations, like ``m`` for
        meters, are also supported. For variables with compound units,
        each unit name is separated by a single space, with exponents
        other than 1 placed immediately after the name, as in ``m s-1``
        for velocity, ``W m-2`` for an energy flux, or ``km2`` for an
        area.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        Returns
        -------
        str
            The variable units.
        Notes
        -----
        CSDMS uses the `UDUNITS`_ standard from Unidata.
        .. _UDUNITS: http://www.unidata.ucar.edu/software/udunits
        """
        return self.implementation.get_var_units(self.state, name)

    def get_var_itemsize(self, name: str) -> int:
        """Get memory use for each array element in bytes.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        Returns
        -------
        int
            Item size in bytes.
        """
        return self.implementation.get_var_itemsize(self.state, name)

    def get_var_nbytes(self, name: str) -> int:
        """Get size, in bytes, of the given variable.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        Returns
        -------
        int
            The size of the variable, counted in bytes.
        """
        return self.implementation.get_var_nbytes(self.state, name)

    def get_var_location(self, name: str) -> str:
        """Get the grid element type that the a given variable is defined on.
        The grid topology can be composed of *nodes*, *edges*, and *faces*.
        *node*
            A point that has a coordinate pair or triplet: the most
            basic element of the topology.
        *edge*
            A line or curve bounded by two *nodes*.
        *face*
            A plane or surface enclosed by a set of edges. In a 2D
            horizontal application one may consider the word “polygon”,
            but in the hierarchy of elements the word “face” is most common.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        Returns
        -------
        str
            The grid location on which the variable is defined. Must be one of
            `"node"`, `"edge"`, or `"face"`.
        Notes
        -----
        CSDMS uses the `ugrid conventions`_ to define unstructured grids.
        .. _ugrid conventions: http://ugrid-conventions.github.io/ugrid-conventions
        """
        return self.implementation.get_var_location(self.state, name)

    def get_current_time(self) -> float:
        """Current time of the model.
        Returns
        -------
        float
            The current model time.
        """
        return self.implementation.get_current_time(self.state)

    def get_start_time(self) -> float:
        """Start time of the model.
        Model times should be of type float.
        Returns
        -------
        float
            The model start time.
        """
        return self.implementation.get_start_time(self.state)

    def get_end_time(self) -> float:
        """End time of the model.
        Returns
        -------
        float
            The maximum model time.
        """
        return self.implementation.get_end_time(self.state)

    def get_time_units(self) -> str:
        """Time units of the model.
        Returns
        -------
        str
            The model time unit; e.g., `days` or `s`.
        Notes
        -----
        CSDMS uses the UDUNITS standard from Unidata.
        """
        return self.implementation.get_time_units(self.state)

    def get_time_step(self) -> float:
        """Current time step of the model.
        The model time step should be of type float.
        Returns
        -------
        float
            The time step used in model.
        """
        return self.implementation.get_time_step(self.state)

    # pylint: disable=arguments-differ
    def get_value(self, name: str) -> np.ndarray:
        """Get a copy of values of the given variable.
        This is a getter for the model, used to access the model's
        current state. It returns a *copy* of a model variable, with
        the return type, size and rank dependent on the variable.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.

        Returns
        -------
        ndarray
            A numpy array containing the requested value(s).
        """
        return np.array(self.implementation.get_value(self.state, name))

    def get_value_ptr(self, name: str) -> np.ndarray:
        """Get a reference to values of the given variable.
        This is a getter for the model, used to access the model's
        current state. It returns a reference to a model variable,
        with the return type, size and rank dependent on the variable.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        Returns
        -------
        array_like
            A reference to a model variable.
        """
        raise NotImplementedError(
            "This method is incompatible with Julia-Python interface"
        )

    # pylint: disable=arguments-differ
    def get_value_at_indices(self, name: str, inds: np.ndarray) -> np.ndarray:
        """Get values at particular indices.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        dest : ndarray
            A numpy array into which to place the values.
        inds : array_like
            The indices into the variable array.
        Returns
        -------
        array_like
            Value of the model variable at the given location.
        """
        if np.any(inds == 0):
            raise ValueError(
                "Julia indices start at 1. Please adjust your indices accordingly."
            )

        return np.array(
            self.implementation.get_value_at_indices(
                self.state, name, jl.convert(jl.Vector[jl.Int64], inds)
            )
        )

    def set_value(self, name: str, values: np.ndarray) -> None:
        """Specify a new value for a model variable.
        This is the setter for the model, used to change the model's
        current state. It accepts, through *values*, a new value for a
        model variable, with the type, size and rank of *values*
        dependent on the variable.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        values : array_like
            The new value for the specified variable.
        """
        self.implementation.set_value(self.state, name, jl.convert(jl.Vector, values))

    def set_value_at_indices(
        self, name: str, inds: np.ndarray, src: np.ndarray
    ) -> None:
        """Specify a new value for a model variable at particular indices.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        inds : array_like
            The indices into the variable array.
        src : array_like
            The new value for the specified variable.
        """
        self.implementation.set_value_at_indices(
            self.state,
            name,
            jl.convert(jl.Vector[jl.Int64], inds),
            jl.convert(jl.Vector, src),
        )

    # Grid information
    def get_grid_rank(self, grid: int) -> int:
        """Get number of dimensions of the computational grid.
        Parameters
        ----------
        grid : int
            A grid identifier.
        Returns
        -------
        int
            Rank of the grid.
        """
        return self.implementation.get_grid_rank(self.state, grid)

    def get_grid_size(self, grid: int) -> int:
        """Get the total number of elements in the computational grid.
        Parameters
        ----------
        grid : int
            A grid identifier.
        Returns
        -------
        int
            Size of the grid.
        """
        return self.implementation.get_grid_size(self.state, grid)

    def get_grid_type(self, grid: int) -> str:
        """Get the grid type as a string.
        Parameters
        ----------
        grid : int
            A grid identifier.
        Returns
        -------
        str
            Type of grid as a string.
        """
        return self.implementation.get_grid_type(self.state, grid)

    # Uniform rectilinear
    def get_grid_shape(self, grid: int) -> np.ndarray:
        """Get dimensions of the computational grid.
        Parameters
        ----------
        grid : int
            A grid identifier.

        Returns
        -------
        ndarray of int
            A numpy array that holds the grid's shape.
        """
        return np.array(self.implementation.get_grid_shape(self.state, grid))

    def get_grid_spacing(self, grid: int) -> np.ndarray:
        """Get distance between nodes of the computational grid.
        Parameters
        ----------
        grid : int
            A grid identifier.
        Returns
        -------
        ndarray of float
            A numpy array that holds the grid's spacing between grid rows and columns.
        """
        return np.array(self.implementation.get_grid_spacing(self.state, grid))

    def get_grid_origin(self, grid: int) -> np.ndarray:
        """Get coordinates for the lower-left corner of the computational grid.
        Parameters
        ----------
        grid : int
            A grid identifier.

        Returns
        -------
        ndarray of float
            A numpy array that holds the coordinates of the grid's
            lower-left corner.
        """
        return np.array(self.implementation.get_grid_origin(self.state, grid))

    # Non-uniform rectilinear, curvilinear
    def get_grid_x(self, grid: int) -> np.ndarray:
        """Get coordinates of grid nodes in the x direction.
        Parameters
        ----------
        grid : int
            A grid identifier.

        Returns
        -------
        ndarray of float
            The input numpy array that holds the grid's column x-coordinates.
        """
        return np.array(self.implementation.get_grid_x(self.state, grid))

    def get_grid_y(self, grid: int) -> np.ndarray:
        """Get coordinates of grid nodes in the y direction.
        Parameters
        ----------
        grid : int
            A grid identifier.

        Returns
        -------
        ndarray of float
            The input numpy array that holds the grid's row y-coordinates.
        """
        return np.array(self.implementation.get_grid_y(self.state, grid))

    def get_grid_z(self, grid: int) -> np.ndarray:
        """Get coordinates of grid nodes in the z direction.
        Parameters
        ----------
        grid : int
            A grid identifier.
        z : ndarray of float, shape *(nlayers,)*
            A numpy array to hold the z-coordinates of the grid nodes layers.
        Returns
        -------
        ndarray of float
            The input numpy array that holds the grid's layer z-coordinates.
        """
        return np.array(self.implementation.get_grid_z(self.state, grid))

    def get_grid_node_count(self, grid: int) -> int:
        """Get the number of nodes in the grid.
        Parameters
        ----------
        grid : int
            A grid identifier.
        Returns
        -------
        int
            The total number of grid nodes.
        """
        return self.implementation.get_grid_node_count(self.state, grid)

    def get_grid_edge_count(self, grid: int) -> int:
        """Get the number of edges in the grid.
        Parameters
        ----------
        grid : int
            A grid identifier.
        Returns
        -------
        int
            The total number of grid edges.
        """
        return self.implementation.get_grid_edge_count(self.state, grid)

    def get_grid_face_count(self, grid: int) -> int:
        """Get the number of faces in the grid.
        Parameters
        ----------
        grid : int
            A grid identifier.
        Returns
        -------
        int
            The total number of grid faces.
        """
        return self.implementation.get_grid_face_count(self.state, grid)

    def get_grid_edge_nodes(self, grid: int) -> np.ndarray:
        """Get the edge-node connectivity.
        Parameters
        ----------
        grid : int
            A grid identifier.

        Returns
        -------
        ndarray of int, shape *(2 x nnodes,)*
            A numpy array that holds the edge-node connectivity. For each edge,
            connectivity is given as node at edge tail, followed by node at
            edge head.
        """
        return np.array(self.implementation.get_grid_edge_nodes(self.state, grid))

    def get_grid_face_edges(self, grid: int) -> np.ndarray:
        """Get the face-edge connectivity.

        Parameters
        ----------
        grid : int
            A grid identifier.

        Returns
        -------
        ndarray of int
            A numpy array that holds the face-edge connectivity.
        """
        return np.array(self.implementation.get_grid_face_edges(self.state, grid))

    def get_grid_face_nodes(self, grid: int) -> np.ndarray:
        """Get the face-node connectivity.

        Parameters
        ----------
        grid : int
            A grid identifier.

        Returns
        -------
        ndarray of int
            A numpy array that holds the face-node connectivity. For each face,
            the nodes (listed in a counter-clockwise direction) that form the
            boundary of the face.
        """
        return np.array(self.implementation.get_grid_face_nodes(self.state, grid))

    def get_grid_nodes_per_face(self, grid: int) -> np.ndarray:
        """Get the number of nodes for each face.
        Parameters
        ----------
        grid : int
            A grid identifier.
        nodes_per_face : ndarray of int, shape *(nfaces,)*
            A numpy array to place the number of nodes per face.
        Returns
        -------
        ndarray of int, shape *(nfaces,)*
            A numpy array that holds the number of nodes per face.
        """
        return np.array(self.implementation.get_grid_nodes_per_face(self.state, grid))
