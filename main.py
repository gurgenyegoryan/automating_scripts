import sys

import subprocess
import ipaddress

us_pass = 'sugg'
user = 'suguest'

ns_ip = '192.168.4.101'
ns_path = '/etc/bind/'
file_rfc = ns_path + 'named.rfc1912.zones'


def up_hosts():
    ipaddress_list = []
    print("Start searching for active ip addresses")
    for ip in ipaddress.IPv4Network('192.168.4.0/24'):
        status, result = subprocess.getstatusoutput("timeout 0.2 ping -c1 " + str(ip))
        if status == 0:
            ipaddress_list.append(str(ip))
    ipaddress_list.remove('192.168.4.101')
    print("Active ip addresses founded")
    return ipaddress_list


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
                   f"@       IN       A        {vpn_ip}\n" \
                   f"www     IN      A        {ip}\n\n"

    hostname_file = f"{ns_path}{hostname}.db"
    with open(hostname_file, "w") as f:
        f.write(host_db_file)
    print(f"{hostname} db file created")


def append_global_zone(hostname):
    global file_rfc
    str_rfc = 'zone "%s" IN {\n' \
              '        type master;\n' \
              '        file "/var/named/%s.db";\n' \
              '        allow-update { none; };\n' \
              '};\n\n' % (hostname, hostname)

    with open(file_rfc, "a") as f:
        f.write(str_rfc)


def get_hostname(user_pass, user_name):
    addresses = up_hosts()
    for ip in addresses:
        try:
            cmd1 = f"sshpass -p {user_pass} ssh -o StrictHostKeyChecking=no {user_name}@{ip} uname -n"
            cmd2 = "sshpass -p %s ssh -o StrictHostKeyChecking=no %s@%s /sbin/ifconfig tun0 | grep " \
                   "netmask | awk '{print $2}'" % (
                       user_pass, user_name, str(ip))

            hostname = subprocess.getoutput(cmd1)
            vpn_ip = subprocess.getoutput(cmd2)

        except Exception as e:
            print(f"Can't connect to {ip} host: {e}")
            sys.exit(1)

        finally:
            if ' ' in hostname:
                print(f"Can't connect to host {ip}: {hostname}")
                continue
            elif hostname == '':
                test = subprocess.SubprocessError()
                print(f"In {ip} dont set hostname: {test}")
                continue
            else:
                create_host_file(hostname, ip, vpn_ip)
                append_global_zone(hostname)


get_hostname(us_pass, user)
