#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
import math

folder = 'scream/ResultsTest3/'
data = read_csv(folder + 'test.csv', header=0)
data = data.iloc[100:-100, :]
print(data.head())
data = data[['Time [s]', 'RTT [s]', 'Bytes in flight [byte]', 'Media coder bitrate [bps]', 'Transmitted bitrate [bps]', 'Lost bitrate [bps]', 'CE Marked bitrate [bps]']]
print(data.head())

plt.figure()
plt.plot(data['Time [s]'], data['Media coder bitrate [bps]'])
plt.title('Plot for encoder bitrate')
plt.xlabel('Time (s)')
plt.ylabel('Media coder bitrate (bps)')
plt.savefig(folder + 'encoder_bitrate.png')

plt.figure()
plt.plot(data['Time [s]'], data['RTT [s]'])
plt.title('Plot for latency')
plt.xlabel('Time (s)')
plt.ylabel('RTT (s)')
plt.savefig(folder + 'rtt.png')

plt.figure()
plt.plot(data['Time [s]'], data['Transmitted bitrate [bps]'])
plt.title('Plot for transmitted bitrate')
plt.xlabel('Time (s)')
plt.ylabel('Transmitted bitrate (bps)')
plt.savefig(folder + 'transmitted_bitrate.png')

plt.figure()
plt.plot(data['Time [s]'], data['Lost bitrate [bps]'])
plt.title('Plot for packet loss bitrate')
plt.xlabel('Time (s)')
plt.ylabel('Packet loss bitrate (bps)')
plt.savefig(folder + 'lost_bitrate.png')

plt.figure()
plt.plot(data['Time [s]'], data['CE Marked bitrate [bps]'])
plt.title('Plot for marked packet bitrate')
plt.xlabel('Time (s)')
plt.ylabel('Marked packet bitrate (bps)')
plt.savefig(folder + 'marked_bitrate.png')

plt.figure()
plt.plot(data['Time [s]'], data['Bytes in flight [byte]'])
plt.title('Plot for bytes in flight')
plt.xlabel('Time (s)')
plt.ylabel('Packets in flight (bytes)')
plt.savefig(folder + 'flight_bitrate.png')



data1 = data.loc[data['Time [s]'] > 59]
data1 = data1.loc[data1['Time [s]'] < 65] 
plt.figure()
plt.plot(data1['Time [s]'], data1['Media coder bitrate [bps]'])
plt.title('Plot for encoder bitrate')
plt.xlabel('Time (s)')
plt.ylabel('Media coder bitrate (bps)')
plt.savefig(folder + 'encoder_bitrate_zoom1.png')

plt.figure()
plt.plot(data1['Time [s]'], data1['RTT [s]'])
plt.title('Plot for latency')
plt.xlabel('Time (s)')
plt.ylabel('RTT (s)')
plt.savefig(folder + 'rtt_zoom1.png')

plt.figure()
plt.plot(data1['Time [s]'], data1['Transmitted bitrate [bps]'])
plt.title('Plot for transmitted bitrate')
plt.xlabel('Time (s)')
plt.ylabel('Transmitted bitrate (bps)')
plt.savefig(folder + 'transmitted_bitrate_zoom1.png')

plt.figure()
plt.plot(data1['Time [s]'], data1['Lost bitrate [bps]'])
plt.title('Plot for packet loss bitrate')
plt.xlabel('Time (s)')
plt.ylabel('Packet loss bitrate (bps)')
plt.savefig(folder + 'lost_bitrate_zoom1.png')

plt.figure()
plt.plot(data1['Time [s]'], data1['CE Marked bitrate [bps]'])
plt.title('Plot for marked packet bitrate')
plt.xlabel('Time (s)')
plt.ylabel('Marked packet bitrate (bps)')
plt.savefig(folder + 'marked_bitrate_zoom1.png')

plt.figure()
plt.plot(data1['Time [s]'], data1['Bytes in flight [byte]'])
plt.title('Plot for bytes in flight')
plt.xlabel('Time (s)')
plt.ylabel('Packets in flight (bytes)')
plt.savefig(folder + 'flight_bitrate_zoom1.png')


maxRTTtime = data1['Time [s]'][data1['RTT [s]'].idxmax()]
data1 = data1.loc[data1['Time [s]'] < maxRTTtime]
minRTTtime = data1['Time [s]'][data1['RTT [s]'].idxmin()]
print("Time to spike the RTT -- ", "from:", minRTTtime, "to:", maxRTTtime, "duration:", maxRTTtime - minRTTtime, "s")



data1 = data.loc[data['Time [s]'] > 119]
data1 = data1.loc[data1['Time [s]'] < 125] 
plt.figure()
plt.plot(data1['Time [s]'], data1['Media coder bitrate [bps]'])
plt.title('Plot for encoder bitrate')
plt.xlabel('Time (s)')
plt.ylabel('Media coder bitrate (bps)')
plt.savefig(folder + 'encoder_bitrate_zoom2.png')

plt.figure()
plt.plot(data1['Time [s]'], data1['RTT [s]'])
plt.title('Plot for latency')
plt.xlabel('Time (s)')
plt.ylabel('RTT (s)')
plt.savefig(folder + 'rtt_zoom2.png')

plt.figure()
plt.plot(data1['Time [s]'], data1['Transmitted bitrate [bps]'])
plt.title('Plot for transmitted bitrate')
plt.xlabel('Time (s)')
plt.ylabel('Transmitted bitrate (bps)')
plt.savefig(folder + 'transmitted_bitrate_zoom2.png')

plt.figure()
plt.plot(data1['Time [s]'], data1['Lost bitrate [bps]'])
plt.title('Plot for packet loss bitrate')
plt.xlabel('Time (s)')
plt.ylabel('Packet loss bitrate (bps)')
plt.savefig(folder + 'lost_bitrate_zoom2.png')

plt.figure()
plt.plot(data1['Time [s]'], data1['CE Marked bitrate [bps]'])
plt.title('Plot for marked packet bitrate')
plt.xlabel('Time (s)')
plt.ylabel('Marked packet bitrate (bps)')
plt.savefig(folder + 'marked_bitrate_zoom2.png')

plt.figure()
plt.plot(data1['Time [s]'], data1['Bytes in flight [byte]'])
plt.title('Plot for bytes in flight')
plt.xlabel('Time (s)')
plt.ylabel('Packets in flight (bytes)')
plt.savefig(folder + 'flight_bitrate_zoom2.png')


minBitrateTime = data1['Time [s]'][data1['Media coder bitrate [bps]'].idxmin()]
maxBitrateTime = data['Time [s]'][data['Media coder bitrate [bps]'].idxmax()]
print("Time to spike the bitrate -- ", "from:", minBitrateTime, "to:", maxBitrateTime, "duration:", maxBitrateTime - minBitrateTime, "s")
