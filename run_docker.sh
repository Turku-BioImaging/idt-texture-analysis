#!/bin/bash

rm -rf $(pwd)/results
mkdir -p results images masks
chmod -R 777 results
chmod -R 775 images masks

docker run -it  -v "$(pwd)/images:/code/images" \
    -v "$(pwd)/masks:/code/masks" \
    -v "$(pwd)/results:/code/results" \
    ghcr.io/turku-bioimaging/idt-texture-analysis:0.1.0