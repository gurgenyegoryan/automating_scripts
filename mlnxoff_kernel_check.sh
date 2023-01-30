#!/bin/bash
# https://network.nvidia.com/products/infiniband-drivers/linux/mlnx_ofed/

# save kernel verion in file and load in variable
kernel_version_path=/home/suguest/.config/kernel_version.txt
kern_version=`cat $kernel_version_path`

# Check if version change, uninstall and install mlnx_ofed and rewrite kernel version file with current version
kern_version_now=`uname -r`
if [ "$kern_version_now" != "$kern_version" ]; then
    echo "Uninstall last installed Mellanox Drier..."
    cd /tmp &&
    wget https://content.mellanox.com/ofed/MLNX_OFED-5.8-1.1.2.1/MLNX_OFED_LINUX-5.8-1.1.2.1-ubuntu22.04-x86_64.iso &&
    mkdir -p mlnx &&
    mount -o ro,loop MLNX_OFED_LINUX-5.8-1.1.2.1-ubuntu22.04-x86_64.iso ./mlnx &&
    ./mlnx/uninstall.sh --force &&
    ./mlnx/mlnxofedinstall --without-dkms --add-kernel-support --kernel $(uname -r) --without-fw-update --force &&
    /etc/init.d/openibd restart
    /etc/init.d/opensmd restart
    echo $kern_verion_now > $kernel_version_path
fi
echo "Nothing to do"
# Set in crontab this script and it be run after restart:

# 1. sudo crontab -e
# Add this line
# 2. @reboot {script_path}/.sh

# or create systemd service
