#include <string>
#include <iostream>

#include <grpc/grpc.h>
#include <grpcpp/server.h>
#include <grpcpp/server_builder.h>
#include <grpcpp/server_context.h>
#include <grpcpp/security/server_credentials.h>

#include "bmi-c/heat/bmi_heat.h"
#include "bmi-c/bmi/bmilib.h"
#include "bmi.grpc.pb.h"
#include "bmi.pb.h"
#include "bmi_grpc_server.h"
#include "bmi_c_wrapper.h"

Bmi* create_model_instance()
{
    BMI_Model * model = (BMI_Model*)malloc (sizeof(BMI_Model));
    register_bmi_heat(model);
    BMI_Initialize (model, NULL);
    return new BmiCWrapper(model);
}

void serve(Bmi* model_instance)
{
    std::string server_address("0.0.0.0:50051");
    BmiGRPCService service(model_instance); 
    grpc::ServerBuilder builder;
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);
    std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
    std::cout << "Server listening on " << server_address << std::endl;
    server->Wait();
}

int main(int argc, char* argv[])
{
    std::cout<<"starting..."<<std::endl;
    Bmi* model = create_model_instance();
    serve(model);
    delete model;
    return 0;
}

