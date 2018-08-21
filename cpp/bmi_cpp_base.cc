#include <bmi_cpp_base.h>
#include <algorithm>
#include <locale>

BmiCppBase::BmiCppBase(){}

void BmiCppBase::runModel()
{
    this->UpdateUntil(this->GetEndTime());
}

template<> std::vector<int> BmiCppBase::GetValue(const std::string name) const
{
    if (this->find_type(name) == 'i')
    {
        return this->GetValueInt(name);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not integer");
}

template<> std::vector<float> BmiCppBase::GetValue(const std::string name) const
{
    if (this->find_type(name) == 'f')
    {
        return this->GetValueFloat(name);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not float");
}

template<> std::vector<double> BmiCppBase::GetValue(const std::string name) const
{
    if (this->find_type(name) == 'd')
    {
        return this->GetValueDouble(name);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not double");
}

template<> int* BmiCppBase::GetValuePtr(std::string name)
{
    if (this->find_type(name) == 'i')
    {
        return this->GetValueIntPtr(name);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not integer");
}

template<> float* BmiCppBase::GetValuePtr(std::string name)
{
    if (this->find_type(name) == 'f')
    {
        return this->GetValueFloatPtr(name);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not float");
}

template<> double* BmiCppBase::GetValuePtr(std::string name)
{
    if (this->find_type(name) == 'd')
    {
        return this->GetValueDoublePtr(name);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not double");
}

template<> std::vector<int> BmiCppBase::GetValueAtIndices(std::string name, const std::vector<int>& indices) const
{
    if (this->find_type(name) == 'i')
    {
        return this->GetValueIntAtIndices(name, indices);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not integer");
}

template<> std::vector<float> BmiCppBase::GetValueAtIndices(std::string name, const std::vector<int>& indices) const
{
    if (this->find_type(name) == 'f')
    {
        return this->GetValueFloatAtIndices(name, indices);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not float");
}

template<> std::vector<double> BmiCppBase::GetValueAtIndices(std::string name, const std::vector<int>& indices) const
{
    if (this->find_type(name) == 'd')
    {
        return this->GetValueDoubleAtIndices(name, indices);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not double");
}

template<> void BmiCppBase::SetValue(std::string name, const std::vector<int>& src)
{
    if (this->find_type(name) == 'i')
    {
        this->SetValueInt(name, src);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not integer");
}

template<> void BmiCppBase::SetValue(std::string name, const std::vector<float>& src)
{
    if (this->find_type(name) == 'f')
    {
        this->SetValueFloat(name, src);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not float");
}

template<> void BmiCppBase::SetValue(std::string name, const std::vector<double>& src)
{
    if (this->find_type(name) == 'd')
    {
        this->SetValueDouble(name, src);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not double");
}

template<> void BmiCppBase::SetValuePtr(std::string name, int* const ptr)
{
    if (this->find_type(name) == 'i')
    {
        this->SetValueIntPtr(name, ptr);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not integer");
}

template<> void BmiCppBase::SetValuePtr(std::string name, float* const ptr)
{
    if (this->find_type(name) == 'f')
    {
        this->SetValueFloatPtr(name, ptr);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not float");
}

template<> void BmiCppBase::SetValuePtr(std::string name, double* const ptr)
{
    if (this->find_type(name) == 'd')
    {
        this->SetValueDoublePtr(name, ptr);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not double");
}

template<> void BmiCppBase::SetValueAtIndices(std::string name, const std::vector<int>& indices, const std::vector<int>& values)
{
    if (this->find_type(name) == 'i')
    {
        this->SetValueIntAtIndices(name, indices, values);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not integer");
}

template<> void BmiCppBase::SetValueAtIndices(std::string name, const std::vector<int>& indices, const std::vector<float>& values)
{
    if (this->find_type(name) == 'f')
    {
        this->SetValueFloatAtIndices(name, indices, values);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not float");
}

template<> void BmiCppBase::SetValueAtIndices(std::string name, const std::vector<int>& indices, const std::vector<double>& values)
{
    if (this->find_type(name) == 'd')
    {
        this->SetValueDoubleAtIndices(name, indices, values);
    }
    throw std::invalid_argument("The value type of variable " + name + "is not double");
}

char BmiCppBase::find_type(const std::string& varname) const
{
    std::locale loc;
    std::string vartype = std::tolower(this->GetVarType(varname), loc);
    std::vector<std::string>inttypes = {"int", "int16", "int32", "int64"};
    if(std::find(inttypes.begin(), inttypes.end(), vartype) != inttypes.end())
    {
        return 'i';
    }
    std::vector<std::string>flttypes = {"float", "float32"};
    if(std::find(flttypes.begin(), flttypes.end(), vartype) != flttypes.end())
    {
        return 'f';
    }
    std::vector<std::string>dbltypes = {"double", "float64"};
    if(std::find(dbltypes.begin(), dbltypes.end(), vartype) != dbltypes.end())
    {
        return 'd';
    }
    throw std::invalid_argument("Could not match the variable type " + vartype + " of variable " + varname + "to integer, float or double");
}
