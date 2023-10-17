module FakeModel

import BasicModelInterface as BMI

Base.@kwdef mutable struct Model
end

BMI.initialize(::Type{Model}, config_file) = Model()

BMI.get_component_name(m::Model) = "The 2D Heat Equation"

function BMI.get_grid_x(m::Model, grid, x)
    copyto!(x, [1.0, 2.0])
end

function BMI.get_grid_y(m::Model, grid, y)
    copyto!(y, [3.0, 4.0])
end

function BMI.get_grid_z(m::Model, grid, z)
    copyto!(z, [5.0, 6.0])
end

BMI.get_grid_edge_count(m::Model, grid) = 10
BMI.get_grid_face_count(m::Model, grid) = 11

function BMI.get_grid_edge_nodes(m::Model, grid, edge_nodes)
    copyto!(edge_nodes, [7.0, 8.0])
end

function BMI.get_grid_face_edges(m::Model, grid, face_edges)
    copyto!(face_edges, [9.0, 10.0])
end

function BMI.get_grid_face_nodes(m::Model, grid, face_nodes)
    copyto!(face_nodes, [11.0, 12.0])
end

function BMI.get_grid_nodes_per_face(m::Model, grid, nodes_per_face)
    copyto!(nodes_per_face, [13.0, 14.0])
end

end # FakeModel module
