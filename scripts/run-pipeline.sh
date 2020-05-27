#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
    echo "Setting up the pipeline, this may take a few seconds"
    sudo docker-compose up -d
    alive=$(HEAD http://localhost:5672 | grep '200' | wc -l)
    while [ $alive -eq 0 ]; do
        sleep 1
        alive=$(HEAD http://localhost:5672 | grep '200' | wc -l)
    done
    echo "The pipeline is ready"
}


main "$@"
