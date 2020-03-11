#ifndef BMI_C_WRAPPER_H_INCLUDED
#define BMI_C_WRAPPER_H_INCLUDED

#ifndef BMI_INCLUDED
#define BMI_INCLUDED
#include "bmi-c/bmi.h"
#include "bmi-cxx/bmi.hxx"
#endif
  
typedef Bmi BMIModel;

class BmiCWrapper: public bmi::Bmi
{
  public:
    BmiCWrapper(BMIModel*);
    ~BmiCWrapper();

    // Model control functions.
    virtual void Initialize(const char *config_file) override;
    virtual void Update() override;
    virtual void UpdateUntil(double time) override;
    virtual void Finalize() override;

    // Model information functions.
    virtual void GetComponentName(char * const name) override;
    virtual int GetInputVarNameCount(void) override;
    virtual int GetOutputVarNameCount(void) override;
    virtual void GetInputVarNames(char **names) override;
    virtual void GetOutputVarNames(char **names) override;

    // Variable information functions
    virtual int GetVarGrid(const char *name) override;
    virtual void GetVarType(const char *name, char *vtype) override;
    virtual void GetVarUnits (const char *name, char *units) override;
    virtual int GetVarItemsize(const char *name) override;
    virtual int GetVarNbytes(const char *name) override;
    virtual void GetVarLocation(const char *name, char *location) override;

    virtual double GetCurrentTime(void) override;
    virtual double GetStartTime(void) override;
    virtual double GetEndTime(void) override;
    virtual void GetTimeUnits(char *units) override;
    virtual double GetTimeStep(void) override;

    // Variable getters
    virtual void GetValue(const char *name, void *dest) override;
    virtual void *GetValuePtr(const char *name) override;
    virtual void *GetValueAtIndices(const char *name, void *dest, int *inds, int count) override;

    // Variable setters
    virtual void SetValue(const char *name, void *values) override;
    virtual void SetValueAtIndices(const char *name, void *values, int *inds, int count) override;

    // Grid information functions
    virtual int GetGridRank(const int grid) override;
    virtual int GetGridSize(const int grid) override;
    virtual void GetGridType(const int grid, char *gtype) override;

    virtual void GetGridShape(const int grid, int *shape) override;
    virtual void GetGridSpacing(const int grid, double *spacing) override;
    virtual void GetGridOrigin(const int grid, double *origin) override;

    virtual void GetGridX(const int grid, double *dest) override;
    virtual void GetGridY(const int grid, double *dest) override;
    virtual void GetGridZ(const int grid, double *dest) override;

    virtual int GetGridNodeCount(const int grid) override;
    virtual int GetGridEdgeCount(const int grid) override;
    virtual int GetGridFaceCount(const int grid) override;

    virtual void GetGridEdgeNodes(const int grid, int *edge_nodes) override;
    virtual void GetGridFaceEdges(const int grid, int *face_edges) override;
    virtual void GetGridFaceNodes(const int grid, int *face_nodes) override;
    virtual void GetGridNodesPerFace(const int, int *nodes_per_face) override;

  private:
    BMIModel* const model;
};

#endif /*BMI_C_WRAPPER_H_INCLUDED*/
