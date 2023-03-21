#!/bin/bash

# Check nvidia-smi
if ! command -v nvidia-smi &> /dev/null
then
    echo "ERROR: nvidia-smi or diver for gpu is not installed"
    exit 1
fi

# Check for GPU model and save to in variable
GPU_MODEL=$(nvidia-smi --query-gpu=gpu_name --format=csv | tail -n +2)
if echo "$GPU_MODEL" | grep -qi "V100"
then
   GPU_TYPE="V100"
elif echo "$GPU_MODEL" | grep -qi "A100"
then
   GPU_TYPE="A100"
elif echo "$GPU_MODEL" | grep -qi "A10"
then
   GPU_TYPE="A10"
else
   GPU_TYPE="Unknown"
fi

echo "Detected Nvidia GPU model: $GPU_TYPE"
