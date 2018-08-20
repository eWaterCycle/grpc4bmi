#ifndef BMI_H_INCLUDED
#define BMI_H_INCLUDED

#include <string>


class Bmi {
  public:
    Bmi();
    virtual ~Bmi();
    virtual void Initialize (std::string configfile) = 0;
    virtual void Update() = 0;
    virtual void UpdateUntil(double time) = 0;
    virtual void UpdateFrac(double time) = 0;
    virtual void Finalize() = 0;
    virtual void GetComponentName(char* name) = 0;
    virtual void GetInputVarNameCount(int* count) = 0;
    virtual void GetOutputVarNameCount(int* count) = 0;
    virtual void GetInputVarNames(char** names) = 0;
    virtual void GetOutputVarNames(char** names) = 0;
    virtual void GetVarType(const char* name, char* type) = 0;
    virtual void GetVarItemsize(const char* name, int* itemsize) = 0;
    virtual void GetVarUnits(const char* name, char* units) = 0;
    virtual void GetVarRank(const char* name, int* rank) = 0;
    virtual void GetVarSize(const char* name, int* size) = 0;
    virtual void GetVarNbytes(const char* name, int* nbytes) = 0;
    virtual void GetCurrentTime(double* time) = 0;
    virtual void GetStartTime(double* start) = 0;
    virtual void GetEndTime(double* end) = 0;
    virtual void GetTimeStep(double* dt) = 0;
    virtual void GetTimeUnits(char* units) = 0;
    virtual void GetValue(const char* name, char* dest) = 0;
    virtual void GetValuePtr(const char* name, char** dest) = 0;
    virtual void GetValueAtIndices(const char* name, char* dest, int* inds, int len) = 0;
    virtual void SetValue(const char* name, char* src) = 0;
    virtual void SetValuePtr(const char* name, char** src) = 0;
    virtual void SetValueAtIndices(const char* name, int* inds, int len, char* src) = 0;
    virtual void GetGridType(const char* name, char* dest) = 0;
    virtual void GetGridShape(const char* name, int* dest) = 0;
    virtual void GetGridSpacing(const char* name, double* dest) = 0;
    virtual void GetGridOrigin(const char* name, double* dest) = 0;
    virtual void GetGridX(const char* name, double* dest) = 0;
    virtual void GetGridY(const char* name, double* dest) = 0;
};

#endif