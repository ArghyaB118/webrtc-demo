#!/bin/bash
set -x

echo "Experiment run on:" $(date)
network_interface="eno1"

# delete any preexisting constraint on network BW
# tc qdisc del dev $network_interface root #not needed anymore

# tc qdisc del dev $network_interface root
# tc qdisc add dev $network_interface root handle 1:0 cbq bandwidth 30Mbit avpkt 1000 cell 8
# tc class add dev $network_interface parent 1:0 classid 1:1 cbq bandwidth 30Mbit rate 30Mbit cell 8 maxburst 20 avpkt 1000 bounded
# tc qdisc add dev $network_interface parent 1:1 dualpi2 limit 100 target 20 tupdate 16000 alpha 0.3125 beta 3.125 l4s_ect coupling_factor 1 drop_on_overload step_thresh 1ms drop_dequeue split_gso classic_protection 10

# make a fresh log file
logfile="scream/test.csv"
#if [[ $logfile != "" && -f $logfile ]]; then
#  rm -v $logfile
#fi
#touch $logfile && echo "created a new log file: test.txt"

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
    tc qdisc change dev $network_interface root handle 1:0 tbf rate $BW"kbit" limit $BW"kbit" burst $BW"kbit"
    tc -s qdisc ls dev $network_interface
    sleep $interval
  done
  pkill -9 scream_bw_test_
}

function generate_plots() {
	for (( i=0; i<=12; i=i+1 ))
	do	
		sleep 15
		python3 test-plots.py
	done
}


function send_prediction() {
	{ echo 30000; sleep 60; echo 1000; sleep 60; echo 30000; sleep 60; echo exit; } | telnet localhost 54000
}


function network_sanity_test2() {
   tc qdisc del dev $network_interface root
	tc qdisc add dev $network_interface root handle 1:0 htb
	tc class add dev $network_interface parent 1:0 classid 1:1 htb rate 30Mbit burst 30Mbit ceil 30Mbit
	tc filter add dev $network_interface parent 1:0 protocol ip prio 1 u32 match ip dst 192.168.18.123/32 flowid 1:1
	sleep 62
	tc qdisc del dev $network_interface root
	tc qdisc add dev $network_interface root handle 1:0 htb
	tc class add dev $network_interface parent 1:0 classid 1:1 htb rate 30Mbit burst 1Mbit ceil 1Mbit
	tc filter add dev $network_interface parent 1:0 protocol ip prio 1 u32 match ip dst 192.168.18.123/32 flowid 1:1
   sleep 60
   tc qdisc del dev $network_interface root
	tc qdisc add dev $network_interface root handle 1:0 htb
	tc class add dev $network_interface parent 1:0 classid 1:1 htb rate 30Mbit burst 30Mbit ceil 30Mbit
	tc filter add dev $network_interface parent 1:0 protocol ip prio 1 u32 match ip dst 192.168.18.123/32 flowid 1:1
	sleep 60
}

function network_sanity_test() {
#	lifespan=180
	tc qdisc del dev $network_interface root
   tc qdisc add dev $network_interface root handle 1:0 tbf rate 30000kbit limit 30000kbit burst 30000kbit
   sleep 60
#	cp $logfile scream/test2.csv
#	python3 test-plots.py
#	tc class change dev $network_interface parent 1:0 classid 1:1 cbq bandwidth 1Mbit rate 1Mbit cell 8 maxburst 20 avpkt 1000 bounded
   tc qdisc change dev $network_interface root handle 1:0 tbf rate 1000kbit limit 1000kbit burst 1000kbit
   sleep 60
#	cp $logfile scream/test2.csv
#	python3 test-plots.py
#  tc class change dev $network_interface parent 1:0 classid 1:1 cbq bandwidth 30Mbit rate 30Mbit cell 8 maxburst 20 avpkt 1000 bounded
 	tc qdisc change dev $network_interface root handle 1:0 tbf rate 30000kbit limit 30000kbit burst 30000kbit
	sleep 60
#	cp $logfile scream/test2.csv
#	python3 test-plots.py
}

read_network_profile

# run the scream server & network throttling in parallel
# generate_plots &
send_prediction &
network_sanity_test & 
#network_e2e &
./scream/bin/scream_bw_test_tx -ect 1 -predictor 0 -fps 60 -log $logfile -itemlist -detailed -time $((lifespan+3*interval)) -if $network_interface 192.168.18.123 8080
wait

