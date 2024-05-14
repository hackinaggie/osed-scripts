#!/bin/sh
# Check if a hostname is provided as an argument
if [ $# -eq 0 ]; then
    hostname="osed"
else
    hostname="$1"
fi

# Resolve the hostname to an IP address using 'getent'
ip_address=$(getent hosts "$hostname" | awk '{print $1}' | head -n1)

if [ -z "$ip_address" ]; then
    echo "Hostname '$hostname' could not be resolved to an IP address."
    exit 1
fi

# Input usernames
if [ $# -eq 3 ]; then
    username="$2"
    password="$3"
else
    username="Offsec"
    password="lab"
fi

cd "$(dirname "$0")"
echo "Connecting to $hostname with $username:$password and sharing the osed-scripts folder as osed-scripts/\n"

# Now construct the xfreerdp command with the resolved IP address, username, and password
xfreerdp +nego +sec-rdp +sec-tls +sec-nla \
    /u:"$username" /p:"$password" /v:"$ip_address" /cert:ignore \
    /dynamic-resolution /tls-seclevel:0 /drive:osed-scripts,.