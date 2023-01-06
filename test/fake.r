library(R6)

FakeFailingRModel <- R6Class(
  public = list(
    # R6 constructor is also called initialize so rename bmi initialize
    bmi_initialize = function(config_file) stop('Always fails'),
    update = function() stop('Always fails'),
    updateUntil = function(until) stop('Always fails'),
    # R6 destructor is also called finalize so rename bmi finalize
    bmi_finalize = function() stop('Always fails'),
    runModel = function() stop('Always fails'),

    getComponentName = function() stop('Always fails'),
    getInputItemCount = function() stop('Always fails'),
    getOutputItemCount = function() stop('Always fails'),  
    getInputVarNames = function() stop('Always fails'),
    getOutputVarNames = function() stop('Always fails'),

    getTimeUnits = function() stop('Always fails'),
    getTimeStep = function() stop('Always fails'),
    getCurrentTime = function() stop('Always fails'),
    getStartTime = function() stop('Always fails'),
    getEndTime = function() stop('Always fails'),

    getVarGrid = function(name) stop('Always fails'),
    getVarType = function(name) stop('Always fails'),
    getVarItemSize = function(name) stop('Always fails'),
    getVarUnits = function(name) stop('Always fails'),
    getVarNBytes = function(name) stop('Always fails'),
    getVarLocation = function(name) stop('Always fails'),

    getValue = function(name) stop('Always fails'),
    getValueAtIndices = function(name, indices) stop('Always fails'),

    setValue = function(name, values) stop('Always fails'),
    setValueAtIndices = function(name, indices, values) stop('Always fails'),

    getGridSize = function(grid_id) stop('Always fails'),
    getGridType = function(grid_id) stop('Always fails'),
    getGridRank = function(grid_id) stop('Always fails'),
    getGridShape = function(grid_id) stop('Always fails'),
    getGridSpacing = function(grid_id) stop('Always fails'),
    getGridOrigin = function(grid_id) stop('Always fails'),
    getGridX = function(grid_id) stop('Always fails'),
    getGridY = function(grid_id) stop('Always fails'),
    getGridZ = function(grid_id) stop('Always fails'),
    getGridNodeCount = function(grid_id) stop('Always fails'),
    getGridEdgeCount = function(grid_id) stop('Always fails'),
    getGridFaceCount = function(grid_id) stop('Always fails'),
    getGridEdgeNodes = function(grid_id) stop('Always fails'),
    getGridFaceNodes = function(grid_id) stop('Always fails'),
    getGridFaceEdges = function(grid_id) stop('Always fails'),
    getGridNodesPerFace = function(grid_id) stop('Always fails')
  )
)
