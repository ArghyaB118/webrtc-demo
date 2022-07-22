#!/bin/bash
set -x

echo "Experiment run on:" $(date)
network_interface="enx0050b61c1cf9" # "lo"

# delete any preexisting constraint on network BW
# tc qdisc del dev $network_interface root #not needed anymore

# read the BW profile
declare -a profile=()
profile_file="profile.txt"

# this function reads the network BW profile generated externally
function read_network_profile() {
  counter=0
  while read -r line; do
    profile[$counter]="$line"
    ((counter++))
  done <$profile_file
echo "${profile[@]}"
}

lifespan=100 # it has to be <= the one defined in the python script
interval=5 # it has to be == the one defined in the python script

# the network function to fluctuate BW
function network_e2e() {
  counter=0
  for (( instant=0; instant<=$lifespan; instant=instant+$interval ))
  do
    BW=$((profile[$counter]))
    ((counter++))
    tc qdisc change dev $network_interface root handle 1:0 tbf rate $BW limit $BW burst $BW
    tc -s qdisc ls dev $network_interface
    sleep $interval
  done
  # pkill -9 chromium-
}

read_network_profile

touch ping-stat.csv
# check this: https://phoenixnap.com/kb/linux-ping-command-examples
#cd samples/
# run the scream server & network throttling in parallel
network_e2e &
ping -i 0.25 -s 100 -w $lifespan 192.168.100.37 >> ping-stat.csv
wait
#npm start
