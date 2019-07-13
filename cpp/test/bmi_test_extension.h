#ifndef BMI_TEST_EXTENSION_H_INCLUDED
#define BMI_TEST_EXTENSION_H_INCLUDED

#include "bmi_cpp_extension.h"

class BmiTestExtension: public BmiCppExtension
{
    public:

        BmiTestExtension(const std::vector<double>&, const std::vector<double>&);
        virtual ~BmiTestExtension();
        
        void Initialize(const std::string& configfile) override;
        void Update() override;
        void UpdateUntil(double time) override;
        void Finalize() override;

        std::string GetComponentName() const override;
        std::vector<std::string> GetInputVarNames() const override;
        std::vector<std::string> GetOutputVarNames() const override;

        int GetVarGrid(const std::string& name) const override;
        std::string GetVarType(const std::string& name) const override;
        int GetVarItemsize(const std::string& name) const override;
        std::string GetVarUnits(const std::string& name) const override;
        int GetVarNbytes(const std::string& name) const override;
        std::string GetVarLocation(const std::string& name) const override;
        double GetCurrentTime() override;
        double GetStartTime() override;
        double GetEndTime() override;
        std::string GetTimeUnits() const override;
        double GetTimeStep() override;
        
        int GetGridRank(int id) override;
        int GetGridSize(int id) override;
        std::string GetGridType(int id) const override;
        std::vector<int> GetGridShape(int id) const override;
        std::vector<double> GetGridSpacing(int id) const override;
        std::vector<double> GetGridOrigin(int id) const override;

        std::vector<double> GetGridX(int id) const override;
        std::vector<double> GetGridY(int id) const override;
        std::vector<double> GetGridZ(int id) const override;

        int GetGridNodeCount(int id) override;
        int GetGridEdgeCount(int id) override;
        int GetGridFaceCount(int id) override;

        std::vector<int> GetGridEdgeNodes(int id) const override;
        std::vector<int> GetGridFaceEdges(int id) const override;
        std::vector<int> GetGridFaceNodes(int id) const override;
        std::vector<int> GetGridNodesPerFace(int id) const override;

    protected:

        std::vector<int> GetValueInt(const std::string& name) const override;
        std::vector<float> GetValueFloat(const std::string& name) const override;
        std::vector<double> GetValueDouble(const std::string& name) const override;

        int* GetValueIntPtr(const std::string& name) override;
        float* GetValueFloatPtr(const std::string& name) override;
        double* GetValueDoublePtr(const std::string& name) override;

        std::vector<int> GetValueIntAtIndices(const std::string& name, const std::vector<int>& indices) const override;
        std::vector<float> GetValueFloatAtIndices(const std::string& name, const std::vector<int>& indices) const override;
        std::vector<double> GetValueDoubleAtIndices(const std::string& name, const std::vector<int>& indices) const override;

        void SetValueInt(const std::string& name, const std::vector<int>& src) override;
        void SetValueFloat(const std::string& name, const std::vector<float>& src) override;
        void SetValueDouble(const std::string& name, const std::vector<double>& src) override;

        void SetValueIntAtIndices(const std::string& name, const std::vector<int>& indices, const std::vector<int>& values) override;
        void SetValueFloatAtIndices(const std::string& name, const std::vector<int>& indices, const std::vector<float>& values) override;
        void SetValueDoubleAtIndices(const std::string& name, const std::vector<int>& indices, const std::vector<double>& values) override;
    
    private:

        int time_counter;
        std::vector<double> x;
        std::vector<double> y;
        std::vector<double>::size_type size;
        std::vector<std::string> input_vars;
        std::vector<std::string> output_vars;
        int grid_id;
        std::vector<double> Q;
        std::vector<double> h;

        bool has_var(std::string name) const;
};

#endif
