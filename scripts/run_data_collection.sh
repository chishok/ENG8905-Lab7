#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ENCODER=$(cd "$SCRIPT_DIR/../encoder" && pwd)

cd "$SCRIPT_DIR/.." || exit 1
mkdir -p data

echo "===> Custom Decoder: Rotate knob CW to 360deg, CCW to -360deg, CW to 0deg"
PYTHONPATH=. python3 "${ENCODER}" --user "$USER" --output "data/dataLogCustom" --custom-decoder

echo "===> Packaged Decoding: Rotate knob CW to 360deg, CCW to -360deg, CW to 0deg"
PYTHONPATH=. python3 "${ENCODER}" --user "$USER" --output "data/dataLogEncoder"

echo "===> High Rate Custom Decoder: Rotate knob CW to 360deg, CCW to -360deg, CW to 0deg"
PYTHONPATH=. python3 "${ENCODER}" --user "$USER" --output "data/dataLogCustom200Hz" --step-size 0.005 --custom-decoder

echo "===> High Rate Packaged Decoding: Rotate knob CW to 360deg, CCW to -360deg, CW to 0deg"
PYTHONPATH=. python3 "${ENCODER}" --user "$USER" --output "data/dataLogEncoder200Hz" --step-size 0.005
