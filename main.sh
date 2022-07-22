#!/bin/bash
set -x

echo "Experiment run on:" $(date)
network_interface="enx0050b61c1cf9"

# delete any preexisting constraint on network BW
# tc qdisc del dev $network_interface root #not needed anymore

# make a fresh log file
logfile="Results/test.csv"
if [[ $logfile != "" && -f $logfile ]]; then
  rm -v $logfile
fi
touch $logfile && echo "created a new log file: test.txt"

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

lifespan=200 # it has to be <= the one defined in the python script
interval=5 # it has to be == the one defined in the python script

# the network function to fluctuate BW
function network_e2e() {
  counter=0
  for (( instant=0; instant<=$lifespan; instant=instant+$interval )) # for instant in {0..30..5}
  do
    # Pattern 2: read BW from a pregenerated external file, a sinusoidal profile with random perturbation
    BW=$((profile[$counter]))
    ((counter++))
    
    # Pattern 1: BW fluctuates in a uniformly random manner between 100kbps and 1mbps
    # BW=$((100+$RANDOM%900)) && BW+="kbit" && echo "Network BW is set to: $BW at $instant seconds"
    # echo "Network BW is set to: $BW at $instant seconds" >> $logfile
    
    # tc qdisc del dev $network_interface root
    # tc qdisc add dev $network_interface root handle 1:0 tbf rate $BW limit $BW burst $BW
    # instead of deleting and adding a new netem qdisc, we modify the existing one
    tc qdisc change dev $network_interface root handle 1:0 tbf rate $BW limit $BW burst $BW
    tc -s qdisc ls dev $network_interface
    sleep $interval
  done
  pkill -9 scream_bw_test_
}

read_network_profile

# run the scream server & network throttling in parallel
network_e2e & 
scream/bin/scream_bw_test_tx -ect 1 -fps 60 -log $logfile -itemlist -detailed -time $((lifespan+3*interval)) -if $network_interface 192.168.100.37 8080
wait

