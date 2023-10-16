module FakeModel

import BasicModelInterface as BMI

Base.@kwdef mutable struct Model
    time::Float64 = 0.0
end

BMI.initialize(::Type{Model}) = Model()

BMI.get_grid_x(m::Model, grid, x)
    copyto!(x, [1.0, 2.0])
end

end
