#!/bin/bash

set -Cue pipefail

PROJECT_HOME="$(cd "$(dirname "${0}")/.." && pwd)"
cd "$PROJECT_HOME"

virtualenv venv
source venv/bin/activate

pip3 install -r requirements.txt
