
#!/bin/bash

# Specify the text to add
cloud_config='/etc/cloud/cloud.cfg'
new_text='chpasswd:
users:
- name: root
password: $(openssl rand -base64 8)
- name: ubuntu
password: $(openssl rand -base64 8)
expire: False'

# Find the line number of the first "users" line
users_line=$(grep -n "^\s*-\s*default$" "$cloud_config" | cut -d':' -f1)
# Find the line number of the next line after the "users" section
next_line=$((users_line + 1))

# Insert the new text after the "users" section
if sed -i "${next_line}r /dev/stdin" <<< "$new_text" "$cloud_config"; then
    echo "New text added to cloud.cfg"
else
    echo "Failed to add new text to cloud.cfg"
fi

# Login root and clear keys
sudo su <<EOF
# Clear authorized keys
if [[ -f ~/.ssh/authorized_keys ]]; then
    echo > ~/.ssh/authorized_keys
    echo "Authorized keys file cleared"
fi

# Securely remove history files
if [[ -f ~/.bash_history ]]; then
    shred -u ~/.bash_history
fi

if [[ -f ~/.zsh_history ]]; then
    shred -u ~/.zsh_history
fi

history -c
echo "Shell history cleared"
EOF


# Move sshd_config file and secure it
if [[ -f sshd_config ]]; then
    mv sshd_config /etc/ssh/sshd_config
    echo "New sshd_config file moved to /etc/ssh/"
    chown root:root /etc/ssh/sshd_config
    chmod 600 /etc/ssh/sshd_config
else
    echo "sshd_config file not found, skipping"
fi

# Lock root user account
passwd -l root
echo "Root account locked"

if [[ -f ~/.ssh/authorized_keys ]]; then
    echo > ~/.ssh/authorized_keys
    echo "Authorized keys file cleared"
fi

# Securely remove SSH keys
if [[ -f /etc/ssh/*_key ]]; then
    sudo shred -u /etc/ssh/*_key /etc/ssh/*_key.pub
    echo "SSH keys securely removed"
else
    echo "No SSH keys found, skipping"
fi


# Securely remove history files
if [[ -f /home/ubuntu/.bash_history ]]; then
    shred -u /home/ubuntu/.bash_history
fi

if [[ -f /home/ubuntu/.zsh_history ]]; then
    shred -u /home/ubuntu/.zsh_history
    echo "Shell history cleared"
fi


# After this delete all script that not needing, and delete history
# do this manual and check all



# rm -Rf ami_based_requirements.sh
# rm -Rf ukv/
# history -c
