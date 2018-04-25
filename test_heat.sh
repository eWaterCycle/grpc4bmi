#!/usr/bin/env bash

echo "Please note for this test to run you need to install bmi with the bmi_heat example"

python run_server.py --name heat.BmiHeat &
bmi-tester bmi_grpc_client.BmiClient