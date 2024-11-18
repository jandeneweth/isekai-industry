#!/bin/bash
# Script to (re)generate the deployable mod.

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo "Script location: ${SCRIPT_DIR}"
STATIC_DIR="${SCRIPT_DIR}/../sources/static"
echo "Static sources directory: ${STATIC_DIR}"
BUILD_DIR="${SCRIPT_DIR}/../build"
echo "Build directory: ${BUILD_DIR}"
BUILD_MOD_DIR="${BUILD_DIR}/isekai-industry"
echo "Build mod directory: ${BUILD_MOD_DIR}"

# Remove the existing files
rm -rf ${BUILD_DIR}/*

# Copy the static files, layering overwrites
cp -rT ${STATIC_DIR}/converted ${BUILD_MOD_DIR}
cp -rT ${STATIC_DIR}/converted_overrides ${BUILD_MOD_DIR}
cp -rT ${STATIC_DIR}/additions ${BUILD_MOD_DIR}
cp -rT ${STATIC_DIR}/metadata ${BUILD_MOD_DIR}

# Run scripts
python ${SCRIPT_DIR}/update_country_histories.py ${BUILD_MOD_DIR}
python ${SCRIPT_DIR}/update_country_definitions.py ${BUILD_MOD_DIR}
python ${SCRIPT_DIR}/update_building_histories.py ${BUILD_MOD_DIR}
python ${SCRIPT_DIR}/update_pops.py ${BUILD_MOD_DIR}