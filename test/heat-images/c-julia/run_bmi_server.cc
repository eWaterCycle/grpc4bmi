// #include "bmi_grpc_server.h"
// #include <bmi.h>
// #include "bmi_heat.h"
#include <julia.h>

int main(int argc, char* argv[])
{
    jl_init();
    {
         {
        // Simple running Julia code

        jl_eval_string("println(sqrt(2.0))");
        }

        // Bmi *model = (Bmi *) malloc(sizeof(Bmi));

        // run_bmi_server(model, argc, argv);
    }
    int ret = 0;
    jl_atexit_hook(ret);
    return ret;
}