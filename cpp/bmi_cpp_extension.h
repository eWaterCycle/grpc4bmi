#ifndef BMI_CPP_EXTENSION_H_INCLUDED
#define BMI_CPP_EXTENSION_H_INCLUDED

#include <string>
#include <vector>
#include <stdexcept>

#ifndef BMI_INCLUDED
#define BMI_INCLUDED
#include "bmi.h"
#include "bmi.hxx"
#endif

class BmiCppExtension: public bmi::Bmi 
{
  public:
      
    BmiCppExtension();
    virtual ~BmiCppExtension();
    virtual void Initialize (const std::string& configfile) = 0;

    virtual std::string GetComponentName() const = 0;
    virtual std::vector<std::string> GetInputVarNames() const = 0;
    virtual std::vector<std::string> GetOutputVarNames() const = 0;

    virtual int GetVarGrid(const std::string& name) const = 0;
    virtual std::string GetVarType(const std::string& name) const = 0;
    virtual int GetVarItemsize(const std::string& name) const = 0;
    virtual std::string GetVarUnits(const std::string& name) const = 0;
    virtual int GetVarNbytes(const std::string& name) const = 0;
    virtual std::string GetVarLocation(const std::string& name) const = 0;
    virtual std::string GetTimeUnits() const = 0;

    virtual std::string GetGridType(int id) const = 0;
    virtual std::vector<int> GetGridShape(int id) const = 0;
    virtual std::vector<double> GetGridSpacing(int id) const = 0;
    virtual std::vector<double> GetGridOrigin(int id) const = 0;

    virtual std::vector<double> GetGridX(int id) const = 0;
    virtual std::vector<double> GetGridY(int id) const = 0;
    virtual std::vector<double> GetGridZ(int id) const = 0;

    virtual std::vector<int> GetGridEdgeNodes(int id) const = 0;
    virtual std::vector<int> GetGridFaceEdges(int id) const = 0;
    virtual std::vector<int> GetGridFaceNodes(int id) const = 0;
    virtual std::vector<int> GetGridNodesPerFace(int id) const = 0;

    template<typename T> std::vector<T> GetValue(const std::string& name)
    {
        std::vector<T> result(this->GetVarNbytes(name.c_str())/sizeof(T));
        this->GetValue(name.c_str(), (void*)result.data());
        return result;
    }
    template<typename T> T* GetValuePtr(const std::string& name)
    {
        return static_cast<T*>(this->GetValuePtr(name.c_str()));
    }
    template<typename T> std::vector<T> GetValueAtIndices(std::string name, std::vector<int>& indices)
    {
        std::vector<T> result(indices.size());
        this->GetValueAtIndices(name.c_str(), (void*)result.data(), indices.data(), indices.size());
        return result;
    }

    template<typename T> void SetValue(std::string name, const std::vector<T>& src)
    {
        this->SetValue(name.c_str(), static_cast<void*>(src.data()));
    }
    template<typename T> void SetValueAtIndices(std::string name, const std::vector<T>& values, std::vector<int>& indices)
    {
        this->SetValueAtIndices(name.c_str(), static_cast<void*>(values.data()), indices.data(), indices.size());
    }

    // Model control functions.
    virtual void Initialize(const char *config_file) override;

    // Model information functions.
    virtual void GetComponentName(char * const name) override;
    virtual int GetInputVarNameCount() override;
    virtual int GetOutputVarNameCount() override;
    virtual void GetInputVarNames(char **names) override;
    virtual void GetOutputVarNames(char **names) override;

    // Variable information functions
    virtual int GetVarGrid(const char *name) override;
    virtual void GetVarType(const char *name, char *vtype) override;
    virtual void GetVarUnits (const char *name, char *units) override;
    virtual int GetVarItemsize(const char *name) override;
    virtual int GetVarNbytes(const char *name) override;
    virtual void GetVarLocation(const char *name, char *location) override;

    virtual void GetTimeUnits(char *units) override;

    // Variable getters
    virtual void GetValue(const char *name, void *dest) override;
    virtual void *GetValuePtr(const char *name) override;
    virtual void *GetValueAtIndices(const char *name, void *dest, int *inds, int count) override;

    // Variable setters
    virtual void SetValue(const char *name, void *values) override;
    virtual void SetValueAtIndices(const char *name, void *values, int *inds, int count) override;

    // Grid information functions
    virtual void GetGridType(int grid, char *gtype) override;

    virtual void GetGridShape(int grid, int *shape) override;
    virtual void GetGridSpacing(int grid, double *spacing) override;
    virtual void GetGridOrigin(int grid, double *origin) override;

    virtual void GetGridX(int grid, double *dest) override;
    virtual void GetGridY(int grid, double *dest) override;
    virtual void GetGridZ(int grid, double *dest) override;

    virtual void GetGridEdgeNodes(int grid, int *dest) override;
    virtual void GetGridFaceEdges(int grid, int *dest) override;
    virtual void GetGridFaceNodes(int grid, int *dest) override;
    virtual void GetGridNodesPerFace(int grid, int *dest) override;

  protected:

    virtual std::vector<int> GetValueInt(const std::string& name) const = 0;
    virtual std::vector<float> GetValueFloat(const std::string& name) const = 0;
    virtual std::vector<double> GetValueDouble(const std::string& name) const = 0;

    virtual int* GetValueIntPtr(const std::string& name) = 0;
    virtual float* GetValueFloatPtr(const std::string& name) = 0;
    virtual double* GetValueDoublePtr(const std::string& name) = 0;

    virtual std::vector<int> GetValueIntAtIndices(const std::string& name, const std::vector<int>& indices) const = 0;
    virtual std::vector<float> GetValueFloatAtIndices(const std::string& name, const std::vector<int>& indices) const = 0;
    virtual std::vector<double> GetValueDoubleAtIndices(const std::string& name, const std::vector<int>& indices) const = 0;

    virtual void SetValueInt(const std::string& name, const std::vector<int>& src) = 0;
    virtual void SetValueFloat(const std::string& name, const std::vector<float>& src) = 0;
    virtual void SetValueDouble(const std::string& name, const std::vector<double>& src) = 0;

    virtual void SetValueIntAtIndices(const std::string& name, const std::vector<int>& indices, const std::vector<int>& values) = 0;
    virtual void SetValueFloatAtIndices(const std::string& name, const std::vector<int>& indices, const std::vector<float>& values) = 0;
    virtual void SetValueDoubleAtIndices(const std::string& name, const std::vector<int>& indices, const std::vector<double>& values) = 0;

  private:

    char FindType(const std::string& name) const;
};

#endif /*BMI_CPP_EXTENSION_H_INCLUDED*/
