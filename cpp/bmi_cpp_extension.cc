#include <algorithm>
#include <cstring>
#include "bmi_cpp_extension.h"

BmiCppExtension::BmiCppExtension(){}

BmiCppExtension::~BmiCppExtension(){}

void BmiCppExtension::GetValue(std::string name, void *dest)
{
    char type = this->FindType(name);
    if(type == 'i')
    {
        std::vector<int> vals = this->GetValueInt(name);
        memcpy(dest, static_cast<void*>(vals.data()), vals.size()*sizeof(int));
    }
    if(type == 'f')
    {
        std::vector<float> vals = this->GetValueFloat(name);
        memcpy(dest, static_cast<void*>(vals.data()), vals.size()*sizeof(float));
    }
    if(type == 'd')
    {
        std::vector<double> vals = this->GetValueDouble(name);
        memcpy(dest, vals.data(), vals.size()*sizeof(double));
    }
}

void* BmiCppExtension::GetValuePtr(std::string name)
{
    char type = this->FindType(name);
    if(type == 'i')
    {
        return static_cast<void*>(this->GetValueIntPtr(name));
    }
    if(type == 'f')
    {
        return static_cast<void*>(this->GetValueFloatPtr(name));
    }
    if(type == 'd')
    {
        return static_cast<void*>(this->GetValueDoublePtr(name));
    }
    return NULL;
}

void BmiCppExtension::GetValueAtIndices(std::string name, void* dest, int* pts, int numpts)
{
    char type = this->FindType(name);
    std::vector<int> indices;
    indices.assign(pts, pts + numpts);
    if(type == 'i')
    {
        std::vector<int> vals = this->GetValueIntAtIndices(name, indices);
        memcpy(dest, static_cast<void*>(vals.data()), vals.size()*sizeof(int));
    }
    if(type == 'f')
    {
        std::vector<float> vals = this->GetValueFloatAtIndices(name, indices);
        memcpy(dest, static_cast<void*>(vals.data()), vals.size()*sizeof(float));
    }
    if(type == 'd')
    {
        std::vector<double> vals = this->GetValueDoubleAtIndices(name, indices);
        memcpy(dest, static_cast<void*>(vals.data()), vals.size()*sizeof(double));
    }
}

void BmiCppExtension::SetValue(std::string name, void* src)
{
    char type = this->FindType(name);
    int nbytes = this->GetVarNbytes(name);
    if(type == 'i')
    {
        std::vector<int> vals;
        vals.assign(static_cast<const int*>(src), static_cast<const int*>(src) + nbytes / sizeof(int));
        this->SetValueInt(name, vals);
    }
    if(type == 'f')
    {
        std::vector<float> vals;
        vals.assign(static_cast<const float*>(src), static_cast<const float*>(src) + nbytes / sizeof(float));
        this->SetValueFloat(name, vals);
    }
    if(type == 'd')
    {
        std::vector<double> vals;
        vals.assign(static_cast<const double*>(src), static_cast<const double*>(src) + nbytes / sizeof(double));
        this->SetValueDouble(name, vals);
    }
}

void BmiCppExtension::SetValueAtIndices(std::string name, int* pts, int numpts, void* src)
{
    char type = this->FindType(name);
    std::vector<int> indices(pts, pts + numpts);
    if(type == 'i')
    {
        std::vector<int> vals;
        vals.assign(static_cast<const int*>(src), static_cast<const int*>(src) + numpts);
        this->SetValueIntAtIndices(name, indices, vals);
    }
    if(type == 'f')
    {
        std::vector<float> vals;
        vals.assign(static_cast<const float*>(src), static_cast<const float*>(src) + numpts);
        this->SetValueFloatAtIndices(name, indices, vals);
    }
    if(type == 'd')
    {
        std::vector<double> vals;
        vals.assign(static_cast<const double*>(src), static_cast<const double*>(src) + numpts);
        this->SetValueDoubleAtIndices(name, indices, vals);
    }

}

void BmiCppExtension::GetGridShape(int id, int* dest)
{
    std::vector<int> shape = this->GetGridShape(id);
    memcpy(dest, shape.data(), shape.size()*sizeof(int));
}

void BmiCppExtension::GetGridSpacing(int id, double* dest)
{
    std::vector<double> s = this->GetGridSpacing(id);
    memcpy(dest, s.data(), s.size()*sizeof(double));
}

void BmiCppExtension::GetGridOrigin(int id, double* dest)
{
    std::vector<double> o = this->GetGridOrigin(id);
    memcpy(dest, o.data(), o.size()*sizeof(double));
}

void BmiCppExtension::GetGridX(int id, double* dest)
{
    std::vector<double> x = this->GetGridX(id);
    memcpy(dest, x.data(), x.size()*sizeof(double));
}

void BmiCppExtension::GetGridY(int id, double* dest)
{
    std::vector<double> x = this->GetGridY(id);
    memcpy(dest, x.data(), x.size()*sizeof(double));
}

void BmiCppExtension::GetGridZ(int id, double* dest)
{
    std::vector<double> x = this->GetGridZ(id);
    memcpy(dest, x.data(), x.size()*sizeof(double));
}

void BmiCppExtension::GetGridEdgeNodes(int grid, int *dest)
{
    std::vector<int> x = this->GetGridEdgeNodes(grid);
    memcpy(dest, x.data(), x.size()*sizeof(double));
}

void BmiCppExtension::GetGridFaceEdges(int grid, int *dest)
{
    std::vector<int> x = this->GetGridFaceEdges(grid);
    memcpy(dest, x.data(), x.size()*sizeof(double));
}

void BmiCppExtension::GetGridFaceNodes(int grid, int *dest)
{
    std::vector<int> x = this->GetGridFaceNodes(grid);
    memcpy(dest, x.data(), x.size()*sizeof(double));
}

void BmiCppExtension::GetGridNodesPerFace(int grid, int *dest)
{
    std::vector<int> x = this->GetGridNodesPerFace(grid);
    memcpy(dest, x.data(), x.size()*sizeof(double));
}

char BmiCppExtension::FindType(const std::string varname)
{
    std::string vartype = this->GetVarType(varname);
    std::transform(vartype.begin(), vartype.end(), vartype.begin(), ::tolower);
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
