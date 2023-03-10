#!/bin/bash

# Prompt user for device name
read -p "Enter device name: " devicename

# Check if device is already mounted and unmount it if necessary
if grep -qs "$devicename" /proc/mounts; then
  sudo umount "$devicename"
fi

# Run fio commands with the device name
sudo fio --filename="$devicename" --size=512GB --direct=1 --rw=randrw --bs=4k --ioengine=io_uring --iodepth=4096 --runtime=120 --numjobs=4 --time_based --group_reporting --name=write_size --eta-newline=1 > random_read_write_file.txt &&
sudo fio --filename="$devicename" --direct=1 --rw=randrw --bs=4k --ioengine=io_uring --iodepth=4096 --runtime=120 --numjobs=4 --time_based --group_reporting --name=write --eta-newline=1 > random_read_write.txt &&
sudo fio --filename="$devicename" --direct=1 --rw=read --bs=4k --ioengine=io_uring --iodepth=4096 --runtime=120 --numjobs=4 --time_based --group_reporting --name=read-sequental > sequental_read.txt &&
sudo fio --filename="$devicename" --direct=1 --rw=randread --bs=4k --ioengine=io_uring --iodepth=4096 --runtime=120 --numjobs=4 --time_based --group_reporting --name=random_read > random_read.txt
