#!/bin/bash

set -Cue pipefail

PROJECT_HOME="$(cd "$(dirname "${0}")/.." && pwd)"
cd "$PROJECT_HOME"

python3 -m grpc_tools.protoc -I proto --python_out=app/peggy --pyi_out=app/peggy --grpc_python_out=app/peggy proto/cp.proto
python3 -m grpc_tools.protoc -I proto --python_out=app/victor --pyi_out=app/victor --grpc_python_out=app/victor proto/cp.proto
