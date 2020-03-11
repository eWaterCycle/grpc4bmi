#ifndef BMI_CPP_EXTENSION_H_INCLUDED
#define BMI_CPP_EXTENSION_H_INCLUDED

#include <string>
#include <vector>
#include <stdexcept>

#ifndef BMI_INCLUDED
#define BMI_INCLUDED
#include "bmi-cxx/bmi.hxx"
#endif

class BmiCppExtension: public bmi::Bmi 
{
  public:
      
    BmiCppExtension();
    virtual ~BmiCppExtension();

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

    template<typename T> std::vector<T> GetValue(const std::string name)
    {
        std::vector<T> result(this->GetVarNbytes(name)/sizeof(T));
        this->GetValue(name, (void*)result.data());
        return result;
    }
    template<typename T> T* GetValuePtr(const std::string& name)
    {
        return static_cast<T*>(this->GetValuePtr(name));
    }
    template<typename T> std::vector<T> GetValueAtIndices(std::string name, std::vector<int>& indices)
    {
        std::vector<T> result(indices.size());
        this->GetValueAtIndices(name, (void*)result.data(), indices.data(), indices.size());
        return result;
    }

    template<typename T> void SetValue(std::string name, const std::vector<T>& src)
    {
        this->SetValue(name, static_cast<void*>(src.data()));
    }
    template<typename T> void SetValueAtIndices(std::string name, const std::vector<T>& values, std::vector<int>& indices)
    {
        this->SetValueAtIndices(name, indices.data(), indices.size(), static_cast<void*>(values.data()));
    }

    // Variable getters
    virtual void GetValue(std::string name, void *dest) override;
    virtual void *GetValuePtr(std::string name) override;
    virtual void GetValueAtIndices(std::string name, void *dest, int *inds, int count) override;

    // Variable setters
    virtual void SetValue(std::string name, void *src) override;
    virtual void SetValueAtIndices(std::string name, int *inds, int count, void *src) override;

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

    char FindType(const std::string name) const;
};

#endif /*BMI_CPP_EXTENSION_H_INCLUDED*/
