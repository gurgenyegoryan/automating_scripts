#!/bin/bash

# Exit on any error

set -e

# Validate user input

read -p "Enter device name: " devicename
read -p "Enter mountpoint: " mountpoint



if [ -e "$devicename" ]; then
    echo "Device $devicename exists"
else
    echo "Device $devicename does not exist"
fi

if [ ! -d "$mountpoint" ]; then
    echo "Mount point not found, now creating mountpoint folder: $mountpoint"
    mkdir "$mountpoint"
fi


# Mount the device if it's not already mounted
if ! grep -qs "$devicename" /proc/mounts; then
    sudo mount "$devicename" "$mountpoint"
fi

# Change to the mount point directory
cd "$mountpoint"

# Run sysbench tests
file_size="512G"
test_mode="rndrw"
max_requests="0"
test_time="300"

echo "Running sysbench tests..."
sysbench fileio --file-total-size="$file_size" --file-test-mode="$test_mode" --time="$test_time" --max-requests="$max_requests" prepare > sysbench_prepare.log
/sbin/sysctl -w vm.drop_caches=3 > /dev/null
sysbench fileio --file-total-size="$file_size" --file-test-mode="$test_mode" --time="$test_time" --max-requests="$max_requests" run > sysbench_run.log
sysbench fileio --file-total-size="$file_size" --file-test-mode="$test_mode" --time="$test_time" --max-requests="$max_requests" cleanup > sysbench_cleanup.log

echo "Sysbench tests completed successfully"
