#include <iostream>
#include <algorithm>
#include <stdexcept>
#include <random>
#include "bmi_test_extension.h"

BmiTestExtension::BmiTestExtension(const std::vector<double>& x_, const std::vector<double>& y_):time_counter(0), x(x_), y(y_), size(x_.size() * y_.size()), input_vars({"water level"}), output_vars({"discharge", "water level"}), grid_id(121)
{
    this->h = std::vector<double>(size, 0.);
    this->Q = std::vector<double>(size, 0.);
    for(std::vector<double>::size_type i = 0; i < size; ++i)
    {
        this->Q[i] = 2500.*((double)std::rand())/RAND_MAX;
        this->h[i] = 2.5*((double)std::rand())/RAND_MAX;
    }
}

void BmiTestExtension::Update()
{
    for(std::vector<double>::size_type i = 0; i < size; ++i)
    {
        this->Q[i] = 2500.*((double)std::rand())/RAND_MAX;
        this->h[i] = 2.5*((double)std::rand())/RAND_MAX;
    }
    this->time_counter++;
}

void BmiTestExtension::UpdateUntil(double t)
{
    while(this->GetCurrentTime() < t)
    {
        this->Update();
    }
}

void BmiTestExtension::Finalize(){}

BmiTestExtension::~BmiTestExtension(){}

void BmiTestExtension::Initialize(const std::string& configfile)
{
    std::cout<<"initializing with "<<configfile;
}

std::string BmiTestExtension::GetComponentName() const
{
    return "test_model";
}

int BmiTestExtension::GetInputItemCount() const
{
    return this->input_vars.size();
}

int BmiTestExtension::GetOutputItemCount() const
{
    return this->output_vars.size();
}

std::vector<std::string> BmiTestExtension::GetInputVarNames() const
{
    return this->input_vars;
}

std::vector<std::string> BmiTestExtension::GetOutputVarNames() const
{
    return this->output_vars;
}

bool BmiTestExtension::has_var(std::string name) const
{
    return std::find(this->input_vars.begin(), this->input_vars.end(), name) != this->input_vars.end() or std::find(this->output_vars.begin(), this->output_vars.end(), name) != this->output_vars.end();
}

int BmiTestExtension::GetVarGrid(const std::string& name) const
{
    if(this->has_var(name))
    {
        return this->grid_id;
    }
    throw std::invalid_argument("unknown variable: " + name);
}

std::string BmiTestExtension::GetVarType(const std::string& name) const
{
    if(this->has_var(name))
    {
        return "double";
    }
    throw std::invalid_argument("unknown variable: " + name);
}

int BmiTestExtension::GetVarItemsize(const std::string& name) const
{
    if(this->has_var(name))
    {
        return sizeof(double);
    }
    throw std::invalid_argument("unknown variable: " + name);
}

std::string BmiTestExtension::GetVarUnits(const std::string& name) const
{
    if(name == "water level")
    {
        return "m";
    }
    if(name == "discharge")
    {
        return "m3 s-1";
    }
    throw std::invalid_argument("unknown variable: " + name);
}

int BmiTestExtension::GetVarNbytes(const std::string& name) const
{
    if(this->has_var(name))
    {
        return sizeof(double) * this->size;
    }
    throw std::invalid_argument("unknown variable: " + name);
}

std::string BmiTestExtension::GetVarLocation(const std::string& name) const
{
    if(name == "water level")
    {
        return "FACE";
    }
    if(name == "discharge")
    {
        return "EDGE";
    }
    throw std::invalid_argument("unknown variable: " + name);
}

double BmiTestExtension::GetCurrentTime()
{
    return this->time_counter;
}

double BmiTestExtension::GetStartTime()
{
    return 0;
}

double BmiTestExtension::GetEndTime()
{
    return 100;
}

std::string BmiTestExtension::GetTimeUnits() const
{
    return "days since 1981-08-29 06:00:00";
}

double BmiTestExtension::GetTimeStep()
{
    return 1;
}

int BmiTestExtension::GetGridRank(int id)
{
    if(id == this->grid_id)
    {
        return 2;
    }
    throw std::invalid_argument("unknown grid id argument");
}

int BmiTestExtension::GetGridSize(int id)
{
    if(id == this->grid_id)
    {
        return this->size;
    }
    throw std::invalid_argument("unknown grid id argument");
}

std::string BmiTestExtension::GetGridType(int id) const
{
    if(id == this->grid_id)
    {
        return "rectilinear";
    }
    throw std::invalid_argument("unknown grid id argument");
}

std::vector<int> BmiTestExtension::GetGridShape(int id) const
{
    if(id == this->grid_id)
    {
        return {static_cast<int>(this->x.size()), static_cast<int>(this->y.size())};
    }
    throw std::invalid_argument("unknown grid id argument");
}


std::vector<double> BmiTestExtension::GetGridSpacing(int id) const
{
    if(id == this->grid_id)
    {
        return std::vector<double>();
    }
    throw std::invalid_argument("unknown grid id argument");
}

std::vector<double> BmiTestExtension::GetGridOrigin(int id) const
{
    if(id == this->grid_id)
    {
        return std::vector<double>();
    }
    throw std::invalid_argument("unknown grid id argument");

}

std::vector<double> BmiTestExtension::GetGridX(int id) const
{
    if(id == this->grid_id)
    {
        return this->x;
    }
    throw std::invalid_argument("unknown grid id argument");

}

std::vector<double> BmiTestExtension::GetGridY(int id) const
{
    if(id == this->grid_id)
    {
        return this->y;
    }
    throw std::invalid_argument("unknown grid id argument");
        
}

std::vector<double> BmiTestExtension::GetGridZ(int id) const
{
    if(id == 1)
    {
        return std::vector<double>(1, 0.);
    }
    throw std::invalid_argument("unknown grid id argument");
    
}

int BmiTestExtension::GetGridNodeCount(int id)
{
    if(id == 1)
    {
        throw std::invalid_argument("grid id does not belong to unstructured grid type");
    }
    throw std::invalid_argument("unknown grid id argument");
}

int BmiTestExtension::GetGridEdgeCount(int id)
{
    if(id == 1)
    {
        throw std::invalid_argument("grid id does not belong to unstructured grid type");
    }
    throw std::invalid_argument("unknown grid id argument");
}

int BmiTestExtension::GetGridFaceCount(int id)
{
    if(id == 1)
    {
        throw std::invalid_argument("grid id does not belong to unstructured grid type");
    }
    throw std::invalid_argument("unknown grid id argument");
}

std::vector<int> BmiTestExtension::GetGridEdgeNodes(int id) const
{
    if(id == 1)
    {
        throw std::invalid_argument("grid id does not belong to unstructured grid type");
    }
    throw std::invalid_argument("unknown grid id argument");
}

std::vector<int> BmiTestExtension::GetGridFaceEdges(int id) const
{
    if(id == 1)
    {
        throw std::invalid_argument("grid id does not belong to unstructured grid type");
    }
    throw std::invalid_argument("unknown grid id argument");
}

std::vector<int> BmiTestExtension::GetGridFaceNodes(int id) const
{
    if(id == 1)
    {
        throw std::invalid_argument("grid id does not belong to unstructured grid type");
    }
    throw std::invalid_argument("unknown grid id argument");
}

std::vector<int> BmiTestExtension::GetGridNodesPerFace(int id) const
{
    if(id == 1)
    {
        throw std::invalid_argument("grid id does not belong to unstructured grid type");
    }
    throw std::invalid_argument("unknown grid id argument");
}

std::vector<int> BmiTestExtension::GetValueInt(const std::string& name) const
{
    throw std::invalid_argument("invalid variable: " + name);
}

std::vector<float> BmiTestExtension::GetValueFloat(const std::string& name) const
{
    throw std::invalid_argument("invalid variable: " + name);
}

std::vector<double> BmiTestExtension::GetValueDouble(const std::string& name) const
{
    if(name == "discharge")
    {
        return this->Q;
    }
    if(name == "water level")
    {
        return this->h;
    }
    throw std::invalid_argument("invalid variable: " + name);
}

int* BmiTestExtension::GetValueIntPtr(const std::string& name)
{
    throw std::invalid_argument("invalid variable: " + name);
}

float* BmiTestExtension::GetValueFloatPtr(const std::string& name)
{
    throw std::invalid_argument("invalid variable: " + name);
}

double* BmiTestExtension::GetValueDoublePtr(const std::string& name)
{
    if(name == "discharge")
    {
        return &(this->Q.data()[0]);
    }
    if(name == "water level")
    {
        return &(this->h.data()[0]);
    }
    throw std::invalid_argument("invalid variable: " + name);
}

std::vector<int> BmiTestExtension::GetValueIntAtIndices(const std::string& name, const std::vector<int>& indices) const
{
    throw std::invalid_argument("invalid variable: " + name);
}

std::vector<float> BmiTestExtension::GetValueFloatAtIndices(const std::string& name, const std::vector<int>& indices) const
{
    throw std::invalid_argument("invalid variable: " + name);
}

std::vector<double> BmiTestExtension::GetValueDoubleAtIndices(const std::string& name, const std::vector<int>& indices) const
{
    const std::vector<double>* ref = NULL;
    if(name == "discharge")
    {
        ref = &(this->Q);
    }
    if(name == "water level")
    {
        ref = &(this->h);
    }
    if(ref == NULL)
    {
        throw std::invalid_argument("invalid variable: " + name);
    }
    std::vector<double>result(indices.size(), 0.);
    for(std::vector<double>::size_type i = 0; i < indices.size(); ++i)
    {
        result[i] = (*ref)[indices[i]];
    }
    return result;
}

void BmiTestExtension::SetValueInt(const std::string& name, const std::vector<int>& src)
{
    throw std::invalid_argument("invalid variable: " + name);
}

void BmiTestExtension::SetValueFloat(const std::string& name, const std::vector<float>& src)
{
    throw std::invalid_argument("invalid variable: " + name);
}

void BmiTestExtension::SetValueDouble(const std::string& name, const std::vector<double>& src)
{
    if(name == "water level")
    {
        for(std::vector<double>::size_type i = 0; i < this->size; ++i)
        {
            this->h[i] = src[i];
        }
    }
    else
    {
        throw std::invalid_argument("invalid variable: " + name);
    }
}

void BmiTestExtension::SetValueIntAtIndices(const std::string& name, const std::vector<int>& indices, const std::vector<int>& values)
{
    throw std::invalid_argument("invalid variable: " + name);
}
void BmiTestExtension::SetValueFloatAtIndices(const std::string& name, const std::vector<int>& indices, const std::vector<float>& values)
{
    throw std::invalid_argument("invalid variable: " + name);
}
void BmiTestExtension::SetValueDoubleAtIndices(const std::string& name, const std::vector<int>& indices, const std::vector<double>& values)
{
    if(name == "water level")
    {
        for(std::vector<double>::size_type i = 0; i < indices.size(); ++i)
        {
            this->h[indices[i]] = values[i];
        }
    }
    else
    {
        throw std::invalid_argument("invalid variable: " + name);    
    }
}
