#!/bin/bash
set -x

echo "Experiment run on:" $(date)
# Note: This may take an additional step to figure out:
# Run the ping command and capture icmp packets on wireshark with filter ip.dst==192.168.18.123
# Figure out which interface is used.
# For me the interface for control plane (100.71.102.x) communication: enxd0374542b1dc
# The interface for data plane (192.168.18.x) communication: eno1
network_interface="eno1"  # "enxd0374542b1dc" # "lo"

# delete any preexisting constraint on network BW outside if tc throws error
sudo tc qdisc del dev $network_interface root
tc qdisc add dev $network_interface root handle 1:0 tbf rate 5000kbit limit 5000kbit burst 5000kbit
sleep 65
tc qdisc change dev $network_interface root handle 1:0 tbf rate 100kbit limit 100kbit burst 100kbit
sleep 60
tc qdisc change dev $network_interface root handle 1:0 tbf rate 5000kbit limit 5000kbit burst 5000kbit
sleep 60
wait


