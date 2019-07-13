#include <algorithm>
#include <cstring>
#include "bmi_cpp_extension.h"

BmiCppExtension::BmiCppExtension(){}

BmiCppExtension::~BmiCppExtension(){}

void BmiCppExtension::Initialize(const char* configfile)
{
    this->Initialize(std::string(configfile));
}

void BmiCppExtension::GetComponentName(char* dest)
{
    std::string s = this->GetComponentName();
    strncpy(dest, s.c_str(), s.size());
    dest[s.size()] = '\0';
}

int BmiCppExtension::GetInputVarNameCount()
{
    return this->GetInputVarNames().size();
}

int BmiCppExtension::GetOutputVarNameCount()
{
    return this->GetOutputVarNames().size();
}

void BmiCppExtension::GetInputVarNames(char** dest)
{
    std::vector<std::string> src = this->GetInputVarNames();
    for(std::vector<std::string>::size_type i = 0; i < src.size(); i++)
    {
        strncpy(dest[i], src[i].c_str(), src[i].size());
        dest[i][src[i].size()] = '\0';
    }
}
    
void BmiCppExtension::GetOutputVarNames(char** dest)
{
    std::vector<std::string> src = this->GetOutputVarNames();
    for(std::vector<std::string>::size_type i = 0; i < src.size(); i++)
    {
        strncpy(dest[i], src[i].c_str(), src[i].size());
        dest[i][src[i].size()] = '\0';
    }
}

void BmiCppExtension::GetVarType(const char* name, char* dest)
{
    std::string type = this->GetVarType(std::string(name));
    strncpy(dest, type.c_str(), type.size());
    dest[type.size()] = '\0';
}

int BmiCppExtension::GetVarItemsize(const char* name)
{
    return this->GetVarItemsize(std::string(name));
}

int BmiCppExtension::GetVarGrid(const char* name)
{
    return this->GetVarGrid(std::string(name));
}

void BmiCppExtension::GetVarUnits(const char* name, char* dest)
{
    std::string units = this->GetVarUnits(std::string(name));
    strncpy(dest, units.c_str(), units.size());
    dest[units.size()] = '\0';
}

int BmiCppExtension::GetVarNbytes(const char* name)
{
    return this->GetVarNbytes(std::string(name));
}

void BmiCppExtension::GetVarLocation(const char *name, char *dest)
{
    std::string loc = this->GetVarLocation(std::string(name));
    strncpy(dest, loc.c_str(), loc.size());
    dest[loc.size()] = '\0';
}

void BmiCppExtension::GetTimeUnits(char* dest)
{
    std::string units = this->GetTimeUnits();
    strncpy(dest, units.c_str(), units.size());
    dest[units.size()] = '\0';
}

void BmiCppExtension::GetValue(const char* name, void* dest)
{
    char type = this->FindType(std::string(name));
    if(type == 'i')
    {
        std::vector<int> vals = this->GetValueInt(std::string(name));
        memcpy(dest, static_cast<void*>(vals.data()), vals.size()*sizeof(int));
    }
    if(type == 'f')
    {
        std::vector<float> vals = this->GetValueFloat(std::string(name));
        memcpy(dest, static_cast<void*>(vals.data()), vals.size()*sizeof(float));
    }
    if(type == 'd')
    {
        std::vector<double> vals = this->GetValueDouble(std::string(name));
        memcpy(dest, vals.data(), vals.size()*sizeof(double));
    }
}

void* BmiCppExtension::GetValuePtr(const char* name)
{
    char type = this->FindType(std::string(name));
    if(type == 'i')
    {
        return static_cast<void*>(this->GetValueIntPtr(std::string(name)));
    }
    if(type == 'f')
    {
        return static_cast<void*>(this->GetValueFloatPtr(std::string(name)));
    }
    if(type == 'd')
    {
        return static_cast<void*>(this->GetValueDoublePtr(std::string(name)));
    }
    return NULL;
}

void* BmiCppExtension::GetValueAtIndices(const char* name, void* dest, int* pts, int numpts)
{
    char type = this->FindType(std::string(name));
    std::vector<int> indices;
    indices.assign(pts, pts + numpts);
    if(type == 'i')
    {
        std::vector<int> vals = this->GetValueIntAtIndices(std::string(name), indices);
        memcpy(dest, static_cast<void*>(vals.data()), vals.size()*sizeof(int));
    }
    if(type == 'f')
    {
        std::vector<float> vals = this->GetValueFloatAtIndices(std::string(name), indices);
        memcpy(dest, static_cast<void*>(vals.data()), vals.size()*sizeof(float));
    }
    if(type == 'd')
    {
        std::vector<double> vals = this->GetValueDoubleAtIndices(std::string(name), indices);
        memcpy(dest, static_cast<void*>(vals.data()), vals.size()*sizeof(double));
    }
    return dest;
}

void BmiCppExtension::SetValue(const char* name, void* src)
{
    char type = this->FindType(std::string(name));
    int nbytes = this->GetVarNbytes(name);
    if(type == 'i')
    {
        std::vector<int> vals;
        vals.assign(static_cast<const int*>(src), static_cast<const int*>(src) + nbytes / sizeof(int));
        this->SetValueInt(std::string(name), vals);
    }
    if(type == 'f')
    {
        std::vector<float> vals;
        vals.assign(static_cast<const float*>(src), static_cast<const float*>(src) + nbytes / sizeof(float));
        this->SetValueFloat(std::string(name), vals);
    }
    if(type == 'd')
    {
        std::vector<double> vals;
        vals.assign(static_cast<const double*>(src), static_cast<const double*>(src) + nbytes / sizeof(double));
        this->SetValueDouble(std::string(name), vals);
    }
}

void BmiCppExtension::SetValueAtIndices(const char* name, void* src, int* pts, int numpts)
{
    char type = this->FindType(std::string(name));
    std::vector<int> indices(pts, pts + numpts);
    if(type == 'i')
    {
        std::vector<int> vals;
        vals.assign(static_cast<const int*>(src), static_cast<const int*>(src) + numpts);
        this->SetValueIntAtIndices(std::string(name), indices, vals);
    }
    if(type == 'f')
    {
        std::vector<float> vals;
        vals.assign(static_cast<const float*>(src), static_cast<const float*>(src) + numpts);
        this->SetValueFloatAtIndices(std::string(name), indices, vals);
    }
    if(type == 'd')
    {
        std::vector<double> vals;
        vals.assign(static_cast<const double*>(src), static_cast<const double*>(src) + numpts);
        this->SetValueDoubleAtIndices(std::string(name), indices, vals);
    }

}

void BmiCppExtension::GetGridType(int id, char* dest)
{
    std::string type = this->GetGridType(id);
    strncpy(dest, type.c_str(), type.size());
    dest[type.size()] = '\0';
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

char BmiCppExtension::FindType(const std::string& varname) const
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
