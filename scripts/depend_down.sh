#!/bin/sh

set -Cue pipefail

PROJECT_HOME="$(cd "$(dirname "${0}")/.." && pwd)"
cd $PROJECT_HOME

docker-compose down redis
