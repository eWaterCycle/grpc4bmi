#!/usr/bin/env bash

# Script showing basic usage of the run-bmi-server executable.

echo "Please note for this test to run you need to install bmi with the bmi_heat example"
trap "kill 0" SIGINT
export BMI_PORT=321123
run-bmi-server --name heat.BmiHeat &
sleep 1 
bmi-tester grpc4bmi.bmi_grpc_client.BmiClient
