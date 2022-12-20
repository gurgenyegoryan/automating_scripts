#!/bin/bash

# save kernel verion in file and load in variable
kern_version_old=`cat /root/var`


# Check if version change, uninstall and install mlnx_ofed and rewrite kernel version file with current version
if [ `uname -r` != "$kern_version" ]; then
    cd /tmp &&
    wget https://content.mellanox.com/ofed/MLNX_OFED-5.8-1.0.1.1/MLNX_OFED_LINUX-5.8-1.0.1.1-ubuntu22.04-x86_64.iso &&
    mkdir -p mlnx &&
    mount -o ro,loop MLNX_OFED_LINUX-5.8-1.0.1.1-ubuntu22.04-x86_64.iso ./mlnx &&
    ./mlnx/uninstall.sh --force &&
    ./mlnx/mlnxofedinstall --without-dkms --add-kernel-support --kernel $(uname -r) --without-fw-update --force &&
    /etc/init.d/openibd restart
    echo `uname -r` > /root/var
fi

# Set in crontab this script and it be run after restart:

# 1. sudo crontab -e
# Add this line
# 2. @reboot {script_path}/.sh