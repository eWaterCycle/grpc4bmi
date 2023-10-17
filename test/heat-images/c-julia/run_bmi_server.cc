// #include "bmi_grpc_server.h"
// #include <bmi.h>
// #include "bmi_heat.h"
#include <iostream>
#include <julia.h>

using namespace std;

int main(int argc, char* argv[])
{
    jl_init();
    {
         {
        // Simple running Julia code
        jl_eval_string("x = sqrt(2.0)");
        jl_eval_string("print(x)");
         }
         {
        jl_eval_string("import Heat");
        }
        {
          jl_function_t *initialize = jl_get_function(jl_main_module, "Heat.BMI.initialize");
          jl_value_t* path = jl_cstr_to_string("/usr/local/share/bmi/heat.toml");
          jl_value_t *model = jl_call1(initialize, path);
          jl_function_t *get_component_name = jl_get_function(jl_main_module, "Heat.BMI.get_component_name");
          jl_value_t *name = jl_call1(get_component_name, model);
          cout << jl_string_ptr(name) << endl;
        }

        // Bmi *model = (Bmi *) malloc(sizeof(Bmi));

        // run_bmi_server(model, argc, argv);
    }
    int ret = 0;
    jl_atexit_hook(ret);
    return ret;
}