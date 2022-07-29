#!/bin/bash
rm -r frames/*.bmp
ffmpeg -i sample-5s.mp4 -vf "select=eq(n\,$1)" -vframes 1 "frames/out.bmp"


