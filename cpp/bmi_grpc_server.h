#ifndef BMI_GRPC_SERVER_H_INCLUDED
#define BMI_GRPC_SERVER_H_INCLUDED

#include "bmi.grpc.pb.h"
#include "bmi-c/bmi.h"
#undef BMI_SUCCESS
#undef BMI_FAILURE
#include "bmi-cxx/bmi.hxx"

typedef bmi::Bmi BmiClass;
typedef Bmi BmiModel;

using bmi::BmiService;

class BmiGRPCService final: public BmiService::Service
{
    public:
        BmiGRPCService(BmiClass*);
        ~BmiGRPCService();
        grpc::Status initialize(grpc::ServerContext* context, const bmi::InitializeRequest* request, bmi::Empty* response) override;
        grpc::Status update(grpc::ServerContext* context, const bmi::Empty* request, bmi::Empty* response) override;
        grpc::Status updateUntil(grpc::ServerContext* context, const bmi::GetTimeResponse* request, bmi::Empty* response) override;
        grpc::Status finalize(grpc::ServerContext* context, const bmi::Empty* request, bmi::Empty* response) override;
        grpc::Status getComponentName(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetComponentNameResponse* response) override;
        grpc::Status getInputItemCount(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetCountResponse* response) override;
        grpc::Status getOutputItemCount(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetCountResponse* response) override;
        grpc::Status getInputVarNames(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNamesResponse* response) override;
        grpc::Status getOutputVarNames(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetVarNamesResponse* response) override;
        grpc::Status getTimeUnits(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeUnitsResponse* response) override;
        grpc::Status getTimeStep(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeStepResponse* response) override;
        grpc::Status getCurrentTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response) override;
        grpc::Status getStartTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response) override;
        grpc::Status getEndTime(grpc::ServerContext* context, const bmi::Empty* request, bmi::GetTimeResponse* response) override;
        grpc::Status getVarGrid(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarGridResponse* response) override;
        grpc::Status getVarType(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarTypeResponse* response) override;
        grpc::Status getVarItemSize(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarItemSizeResponse* response) override;
        grpc::Status getVarLocation(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarLocationResponse* response) override;
        grpc::Status getVarUnits(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarUnitsResponse* response) override;
        grpc::Status getVarNBytes(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetVarNBytesResponse* response) override;
        grpc::Status getValue(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::GetValueResponse* response) override;
        grpc::Status getValuePtr(grpc::ServerContext* context, const bmi::GetVarRequest* request, bmi::Empty* response);
        grpc::Status getValueAtIndices(grpc::ServerContext* context, const bmi::GetValueAtIndicesRequest* request, bmi::GetValueAtIndicesResponse* response) override;
        grpc::Status setValue(grpc::ServerContext* context, const bmi::SetValueRequest* request, bmi::Empty* response) override;
        grpc::Status setValuePtr(grpc::ServerContext* context, const bmi::SetValuePtrRequest* request, bmi::Empty* response);
        grpc::Status setValueAtIndices(grpc::ServerContext* context, const bmi::SetValueAtIndicesRequest* request, bmi::Empty* response) override;
        grpc::Status getGridSize(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridSizeResponse* response) override;
        grpc::Status getGridType(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridTypeResponse* response) override;
        grpc::Status getGridRank(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridRankResponse* response) override;
        grpc::Status getGridShape(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridShapeResponse* response) override;
        grpc::Status getGridSpacing(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridSpacingResponse* response) override;
        grpc::Status getGridOrigin(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridOriginResponse* response) override;
        grpc::Status getGridX(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response) override;
        grpc::Status getGridY(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response) override;
        grpc::Status getGridZ(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridPointsResponse* response) override;
        grpc::Status getGridNodeCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response) override;
        grpc::Status getGridEdgeCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response) override;
        grpc::Status getGridFaceCount(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetCountResponse* response) override;
        grpc::Status getGridEdgeNodes(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridEdgeNodesResponse* response) override;
        grpc::Status getGridFaceNodes(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridFaceNodesResponse* response) override;
        grpc::Status getGridFaceEdges(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridFaceEdgesResponse* response) override;
        grpc::Status getGridNodesPerFace(grpc::ServerContext* context, const bmi::GridRequest* request, bmi::GetGridNodesPerFaceResponse* response) override;
    private:
        BmiClass* const bmi;
        char find_type(const std::string& varname) const;
        void get_grid_dimensions(int id, int* vec3d) const;
        static void process_status(std::string, int);
        static grpc::Status handle_exception(const std::exception&);
};

void run_bmi_server(Bmi* model, int argc, char* argv[]);
void run_bmi_server(BmiClass* model, int argc, char* argv[]);

#endif
