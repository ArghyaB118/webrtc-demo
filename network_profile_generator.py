import math
import random
import os
pi = 3.14159
fp = open('profile.txt', 'w')
period = 40 # period = 40s
interval = 5 # interval = 5s
lifespan = 605 # lifespan of experiment = 600s
# range of BW = 200kbps -- 5mbps
for instant in range(0,lifespan,interval):
  BW = math.floor((2600 + 2400 * math.sin(2 * pi * instant / period)) * random.randint(95,105) / 100) # 0.95--1.05 times chosen randomly, then floor taken
  print("BW is set to ", BW, "at ", instant)
  fp.write(str(BW)+'\n')
fp.close()
