#!/usr/bin/python3
import os, sys
#print(str(sys.argv), sys.argv[0], sys.argv[1])

import imageio

# Get bytes of MKV video
with open('output.mkv', 'rb') as file: 
    content = file.read()

print(sys.getsizeof(content))

