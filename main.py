import sys

import subprocess
import ipaddress

us_pass = 'sugg'
user = 'suguest'
file_rfc = '/etc/named/named.rfc1912.zones'
ns_ip = '192.168.4.101'


def up_hosts():
    ipaddress_list = []

    for ip in ipaddress.IPv4Network('192.168.4.0/32'):
        status, result = subprocess.getstatusoutput("ping -c1 -w2 " + str(ip))  # for linux
        # status, result = subprocess.getstatusoutput("ping -n 1  " + str(ip))  # for windows
        if status == 0:
            ipaddress_list.append(ip)
    ipaddress_list.remove('192.168.4.101')
    return ipaddress_list


def get_hostname(user_pass, user_name):
    addresses = up_hosts()
    for ip in addresses:
        try:
            cmd1 = f"sshpass -p {user_pass} ssh -o StrictHostKeyChecking=no {user_name}@{ip} uname -n"
            cmd2 = "sshpass -p %s ssh -o StrictHostKeyChecking=no %s@%s /sbin/ifconfig tun0 | grep " \
                   "netmask | awk '{print $2}'" % (
                       user_pass, user_name, ip)

            hostname = subprocess.getoutput(cmd1)
            vpn_ip = subprocess.getoutput(cmd2)
            create_host_file(hostname, ip, vpn_ip)
            append_global_zone(hostname)

        except ConnectionError as e:
            print(f"Can't connect to {ip}: {e}")
            sys.exit(1)


def create_host_file(hostname, ip, vpn_ip):
    global ns_ip
    host_db_file = "$TTL 1D\n" \
                   f"$ORIGIN {hostname}.\n" \
                   f"@       IN      SOA     {ns_ip}     root.{ns_ip}. (\n" \
                   "                                            0      ; serial\n" \
                   "                                            1D     ; refresh\n" \
                   "                                            1H     ; retry\n" \
                   "                                            1W     ; expire\n" \
                   "                                            3H )   ; minimum\n" \
                   f"@       IN      NS       {ns_ip}.\n" \
                   f"@       IN      A        {ip}\n" \
                   f"@	     IN	     A	      {vpn_ip}\n" \
                   f"www     IN      A        {ip}\n\n"

    hostname_file = f"/etc/named/{hostname}.db"
    with open(hostname_file, "w") as f:
        f.write(host_db_file)


def append_global_zone(hostname):
    global file_rfc
    str_rfc = 'zone "%s" IN {\n' \
              '        type master;\n' \
              '        file "/var/named/%s.db";\n' \
              '        allow-update { none; };\n' \
              '};\n\n' % (hostname, hostname)

    with open(file_rfc, "a") as f:
        f.write(str_rfc)


get_hostname(us_pass, user)
