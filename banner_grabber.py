 #!/usr/bin/env python3

# Script Name : Banner-Grabber.py 
# Author : Ayan Acharya
# Created : 26-02-2025
# Purpose : Simple Service Banner Grabbing Tool
# Usage : python3 banner.py <IP> <PORT>

import socket
import sys

usage = "\033[1m[+]\033[0m \033[1m\033[32mUsage : python3 banner.py <IP> <PORT>\033[0m\033[0m"
banner = '''\n\033[1m\033[0m \033[1m\033[32m
     ___  ____              ___  ___
    / _/ /   / /|  / /|  / /    / _/  
   / _  / - / / | / / | / /--  / |
  /__/ /   / /  |/ /  |/ /___ /  |
 \033[0m\033[0m
                         \033[0m \033[1m\033[31m@Ayan_Acharya\033[0m\033[31m

'''

# Validate IP Address
def is_valid_ip(ip_str):
    try:
        socket.inet_aton(ip_str)
        return True
    except socket.error:
        return False

# Validate Port Number
def is_valid_port(port_str):
    try:
        port = int(port_str)
        return 0 <= port <= 65535
    except ValueError:
        return False

# Check if arguments are provided
if len(sys.argv) != 3:
    print(banner)
    print(usage)
    sys.exit()

# Get input values
ip = str(sys.argv[1])
port = str(sys.argv[2])

# Validate IP and Port
if not is_valid_ip(ip):
    print("\n\033[1m[+]\033[0m \033[1m\033[31mInvalid IP address. Please provide a valid IP.\033[0m\033[0m")
    sys.exit()
    
if not is_valid_port(port):
    print("\n\033[1m[+]\033[0m \033[1m\033[31mInvalid PORT number. Must be between 0-65535.\033[0m\033[0m")
    sys.exit()

try:
    print(banner)
    print("\n\033[1m[+]\033[0m \033[1m\033[34mConnecting to\033[0m\033[34m", ip, "on port", port, "...\033[0m")
    
    # Create Socket Connection
    s = socket.socket()
    s.settimeout(5)
    s.connect((ip, int(port)))
    
    # Receive Banner
    response = s.recv(1024).decode('utf-8').strip()
    print("\n\033[1m[+]\033[0m \033[1m\033[32mResponse:\033[0m\033[0m", response, "\033[0m\033[0m")
    
except ConnectionRefusedError:
    print("\n\033[1m[+]\033[0m \033[1m\033[31mConnection refused. The port may not be open.\033[0m\033[0m")

except socket.timeout:
    print("\n\033[1m[+]\033[0m \033[1m\033[31mConnection timed out. The target may not be reachable.\033[0m\033[0m")

except Exception as e:
    print("\n\033[1m[+]\033[0m \033[1m\033[31mError:\033[0m\033[0m", str(e))

finally:
    s.close()
