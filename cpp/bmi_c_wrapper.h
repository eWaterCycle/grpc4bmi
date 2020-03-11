#ifndef BMI_C_WRAPPER_H_INCLUDED
#define BMI_C_WRAPPER_H_INCLUDED

#include <string>
#include <vector>

#ifndef BMI_INCLUDED
#define BMI_INCLUDED
#include "bmi-c/bmi.h"
#undef BMI_SUCCESS
#undef BMI_FAILURE
#include "bmi-cxx/bmi.hxx"
#endif
  
typedef Bmi BMIModel;

class BmiCWrapper: public bmi::Bmi
{
  public:
    BmiCWrapper(BMIModel*);
    ~BmiCWrapper();

    // Model control functions.
    virtual void Initialize(std::string config_file) override;
    virtual void Update() override;
    virtual void UpdateUntil(double time) override;
    virtual void Finalize() override;

    // Model information functions.
    virtual std::string GetComponentName() override;
    virtual int GetInputItemCount(void) override;
    virtual int GetOutputItemCount(void) override;
    virtual std::vector<std::string> GetInputVarNames() override;
    virtual std::vector<std::string> GetOutputVarNames() override;

    // Variable information functions
    virtual int GetVarGrid(std::string name) override;
    virtual void GetVarType(std::string name, char *vtype) override;
    virtual void GetVarUnits (std::string name, char *units) override;
    virtual int GetVarItemsize(std::string name) override;
    virtual int GetVarNbytes(std::string name) override;
    virtual void GetVarLocation(std::string name, char *location) override;

    virtual double GetCurrentTime(void) override;
    virtual double GetStartTime(void) override;
    virtual double GetEndTime(void) override;
    virtual void GetTimeUnits(char *units) override;
    virtual double GetTimeStep(void) override;

    // Variable getters
    virtual void GetValue(std::string name, void *dest) override;
    virtual void *GetValuePtr(std::string name) override;
    virtual void *GetValueAtIndices(std::string name, void *dest, int *inds, int count) override;

    // Variable setters
    virtual void SetValue(std::string name, void *values) override;
    virtual void SetValueAtIndices(std::string name, void *values, int *inds, int count) override;

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
