#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <string>

#include <bmi.hxx>
#include <julia.h>
#include "bmi_grpc_server.h"

using namespace std;

class NotImplemented : public std::logic_error
{
public:
    NotImplemented() : std::logic_error("Not Implemented"){};
};

void handle_julia_exception(void) {
    if (jl_value_t *ex = jl_exception_occurred()) {
        jl_printf(jl_stderr_stream(), "Exception:\n");
        jl_call2(
            jl_get_function(jl_base_module, "showerror"),
            jl_stderr_obj(),
            ex
        );
        jl_printf(jl_stderr_stream(), "\nI quit!\n");
        jl_atexit_hook(1);
        exit(1);
    }
}

class BmiJulia : public bmi::Bmi
{
public:
    BmiJulia(std::string package_name, std::string model_name)
    {
        this->modelt = model_name;
        this->package_name = package_name;
    }
    void Initialize(std::string config_file)
    {
        jl_init();
        jl_eval_string("import BasicModelInterface as BMI");
        handle_julia_exception();
        std::string import = "import " + this->package_name;
        // cout << import << endl;
        jl_eval_string(import.c_str());
        handle_julia_exception();

        std::string cmd = "model = BMI.initialize(";
        cmd.append(this->modelt);
        cmd.append(", \"");
        cmd.append(config_file);
        cmd.append("\")");
        // cout << cmd << endl;
        jl_eval_string(cmd.c_str());
        handle_julia_exception();
    }
    

    void Update()
    {
        throw NotImplemented();
    }
    void UpdateUntil(double time)
    {
        throw NotImplemented();
    }
    void Finalize()
    {
        throw NotImplemented();
    }

    std::string GetComponentName()
    {
        cout << "GetComponentName" << jl_is_initialized << endl;
        jl_eval_string("print(model)");
        // If we cant get passed line above 
        // then we are running in another thread 
        // that initialize has not run in
        handle_julia_exception();
        std::string cmd = "BMI.get_component_name(model)";
        cout << cmd << endl;
        jl_value_t *jname = jl_eval_string(cmd.c_str());
        handle_julia_exception();
        const char* cname = jl_string_ptr(jname);
        handle_julia_exception();
        std::string name(cname);
        return name;
    }
    int GetInputItemCount()
    {
        throw NotImplemented();
    }
    int GetOutputItemCount()
    {
        throw NotImplemented();
    }
    std::vector<std::string> GetInputVarNames()
    {
        throw NotImplemented();
    }
    std::vector<std::string> GetOutputVarNames()
    {
        throw NotImplemented();
    }

    int GetVarGrid(std::string name)
    {
        throw NotImplemented();
    }
    std::string GetVarType(std::string name)
    {
        throw NotImplemented();
    }
    int GetVarItemsize(std::string name)
    {
        throw NotImplemented();
    }
    std::string GetVarUnits(std::string name)
    {
        throw NotImplemented();
    }
    int GetVarNbytes(std::string name)
    {
        throw NotImplemented();
    }
    std::string GetVarLocation(std::string name)
    {
        throw NotImplemented();
    }

    double GetCurrentTime()
    {
        throw NotImplemented();
    }
    double GetStartTime()
    {
        throw NotImplemented();
    }
    double GetEndTime()
    {
        throw NotImplemented();
    }
    std::string GetTimeUnits()
    {
        throw NotImplemented();
    }
    double GetTimeStep()
    {
        throw NotImplemented();
    }

    void GetValue(std::string name, void *dest)
    {
        throw NotImplemented();
    }
    void *GetValuePtr(std::string name)
    {
        throw NotImplemented();
    }
    void GetValueAtIndices(std::string name, void *dest, int *inds, int count)
    {
        throw NotImplemented();
    }

    void SetValue(std::string name, void *src)
    {
        throw NotImplemented();
    }
    void SetValueAtIndices(std::string name, int *inds, int len, void *src)
    {
        throw NotImplemented();
    }

    int GetGridRank(const int grid)
    {
        throw NotImplemented();
    }
    int GetGridSize(const int grid)
    {
        throw NotImplemented();
    }
    std::string GetGridType(const int grid)
    {
        throw NotImplemented();
    }

    void GetGridShape(const int grid, int *shape)
    {
        throw NotImplemented();
    }
    void GetGridSpacing(const int grid, double *spacing)
    {
        throw NotImplemented();
    }
    void GetGridOrigin(const int grid, double *origin)
    {
        throw NotImplemented();
    }

    void GetGridX(const int grid, double *x)
    {
        throw NotImplemented();
    }
    void GetGridY(const int grid, double *y)
    {
        throw NotImplemented();
    }
    void GetGridZ(const int grid, double *z)
    {
        throw NotImplemented();
    }

    int GetGridNodeCount(const int grid)
    {
        throw NotImplemented();
    }
    int GetGridEdgeCount(const int grid)
    {
        throw NotImplemented();
    }
    int GetGridFaceCount(const int grid)
    {
        throw NotImplemented();
    }

    void GetGridEdgeNodes(const int grid, int *edge_nodes)
    {
        throw NotImplemented();
    }
    void GetGridFaceEdges(const int grid, int *face_edges)
    {
        throw NotImplemented();
    }
    void GetGridFaceNodes(const int grid, int *face_nodes)
    {
        throw NotImplemented();
    }
    void GetGridNodesPerFace(const int grid, int *nodes_per_face)
    {
        throw NotImplemented();
    }

private:
    std::string modelt;
    std::string package_name;
};

int main(int argc, char *argv[])
{
    {
        {
            // // Simple running Julia code
            // jl_eval_string("x = sqrt(2.0)");
            // jl_eval_string("print(x)");
        }
        {

            /*
            In Julia repl:

            import BasicModelInterface as BMI
            import Heat
            # https://github.com/csdms/bmi-example-julia/raw/main/example/heat.toml
            model = BMI.initialize(Heat.Model, "/usr/local/share/heat.toml")
            BMI.get_component_name(model)

            */
        }
        {
            bmi::Bmi* model = new BmiJulia("Heat", "Heat.Model");
            // Calling without grpc works
            // model->Initialize("/usr/local/share/heat.toml");
            // cout << model->GetComponentName() << endl;

            // Calling from grpc client causes segfault when calling jl_eval_string with BMI.initialize()
            run_bmi_server(model, argc, argv);
        }
    }
    int ret = 0;
    jl_atexit_hook(ret);
    return ret;
}