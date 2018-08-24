#ifndef BMI_H_INCLUDED
#define BMI_H_INCLUDED

#include <string>
#include <vector>
#include <stdexcept>


class BmiCppBase {
  public:
    BmiCppBase();
    virtual ~BmiCppBase();
    virtual void Initialize (std::string configfile) = 0;
    virtual void Update() = 0;
    virtual void UpdateUntil(double time) = 0;
    virtual void UpdateFrac(double time) = 0;
    virtual void runModel();
    virtual void Finalize() = 0;

    virtual std::string GetComponentName() const = 0;
    virtual std::vector<std::string> GetInputVarNames() const = 0;
    virtual std::vector<std::string> GetOutputVarNames() const = 0;
    virtual std::string GetVarType(std::string name) const = 0;
    virtual int GetVarGrid(std::string name) const = 0;
    virtual int GetVarItemSize(std::string name) const = 0;
    virtual std::string GetVarUnits(std::string name) const = 0;
    virtual int GetVarRank(std::string name) const = 0;
    virtual int GetVarSize(std::string name) const = 0;
    virtual int GetVarNbytes(std::string name) const = 0;
    virtual double GetCurrentTime() const = 0;
    virtual double GetStartTime() const = 0;
    virtual double GetEndTime() const = 0;
    virtual double GetTimeStep() const = 0;
    virtual std::string GetTimeUnits() const = 0;

    template<typename T> std::vector<T> GetValue(std::string name) const
    {
        throw std::logic_error(std::string("This method is not generically implemented for type") + std::string(typeid(T).name()));
    }
    template<typename T> T* GetValuePtr(std::string name)
    {
        throw std::logic_error(std::string("This method is not generically implemented for type") + std::string(typeid(T).name()));
    }
    template<typename T> std::vector<T> GetValueAtIndices(std::string name, const std::vector<int>& indices) const
    {
        throw std::logic_error(std::string("This method is not generically implemented for type") + std::string(typeid(T).name()));
    }
    template<typename T> void SetValue(std::string name, const std::vector<T>& src)
    {
        throw std::logic_error(std::string("This method is not generically implemented for type") + std::string(typeid(T).name()));
    }
    template<typename T> void SetValuePtr(std::string name, T* const ptr)
    {
        throw std::logic_error(std::string("This method is not generically implemented for type") + std::string(typeid(T).name()));
    }
    template<typename T> void SetValueAtIndices(std::string name, const std::vector<int>& indices, const std::vector<T>& values)
    {
        throw std::logic_error(std::string("This method is not generically implemented for type") + std::string(typeid(T).name()));
    }

    virtual int GetGridSize(int id) const = 0;
    virtual int GetGridRank(int id) const = 0;
    virtual int GetGridCellCount(int id) const = 0;
    virtual int GetGridPointCount(int id) const = 0;
    virtual int GetGridVertexCount(int id) const = 0;
    virtual std::string GetGridType(int id) const = 0;
    virtual std::vector<int> GetGridShape(int id) const = 0;
    virtual std::vector<int> GetGridConnectivity(int id) const = 0;
    virtual std::vector<double> GetGridSpacing(int id) const = 0;
    virtual std::vector<double> GetGridOrigin(int id) const = 0;
    virtual std::vector<double> GetGridX(int id) const = 0;
    virtual std::vector<double> GetGridY(int id) const = 0;
    virtual std::vector<double> GetGridZ(int id) const = 0;

  protected:

    virtual std::vector<int> GetValueInt(const std::string& name) const = 0;
    virtual std::vector<float> GetValueFloat(const std::string& name) const = 0;
    virtual std::vector<double> GetValueDouble(const std::string& name) const = 0;

    virtual int* GetValueIntPtr(const std::string& name) = 0;
    virtual float* GetValueFloatPtr(const std::string& name) = 0;
    virtual double* GetValueDoublePtr(const std::string& name) = 0;

    virtual std::vector<int> GetValueIntAtIndices(std::string name, const std::vector<int>& indices) const = 0;
    virtual std::vector<float> GetValueFloatAtIndices(std::string name, const std::vector<int>& indices) const = 0;
    virtual std::vector<double> GetValueDoubleAtIndices(std::string name, const std::vector<int>& indices) const = 0;

    virtual void SetValueInt(std::string name, const std::vector<int>& src) = 0;
    virtual void SetValueFloat(std::string name, const std::vector<float>& src) = 0;
    virtual void SetValueDouble(std::string name, const std::vector<double>& src) = 0;

    virtual void SetValueIntPtr(std::string name, int* const ptr) = 0;
    virtual void SetValueFloatPtr(std::string name, float* const ptr) = 0;
    virtual void SetValueDoublePtr(std::string name, double* const ptr) = 0;

    virtual void SetValueIntAtIndices(std::string name, const std::vector<int>& indices, const std::vector<int>& values) = 0;
    virtual void SetValueFloatAtIndices(std::string name, const std::vector<int>& indices, const std::vector<float>& values) = 0;
    virtual void SetValueDoubleAtIndices(std::string name, const std::vector<int>& indices, const std::vector<double>& values) = 0;

  private:

    char find_type(const std::string& name) const;
};

#endif
