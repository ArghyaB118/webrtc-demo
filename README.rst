Machine Setups
==============
Server machine: IP:100.71.102.33 or 192.168.100.33
Client machine: IP:100.71.102.37 or 192.168.100.37

Use the 192.168 channel for cleint-server communication.
Use the 100.71 channel for X2Go connection.

You may have to run the individual experiments out of the main script in order to understand which network interface is being used. Then you may need to change it in the main script accordingly.

Note:
1. scream_receiver.cpp, line 108, rtcpFbInterval_ntp = screamRx->getRtcpFbInterval();
2. scream_receiver.cpp, line 40-41, ackDiff and nReportedRtpPackets


To install the L4S supported linux kernel in the server machine:
.. code-block:: console
    $ git clone https://github.com/L4STeam/linux.git
    $ cd linux
    $ sudo apt install libelf-dev
    $ cp "/boot/config-$(uname -r)" .config
    $ vim .config # delete the flag, make the flag empty CONFIG_SYSTEM_TRUSTED_KEYS="" and unset this flag CONFIG_DEBUG_INFO_BTF=n
    $ make olddefconfig
    $ scripts/config -m TCP_CONG_PRAGUE
    $ scripts/config -m NET_SCH_DUALPI2
    $ ./scripts/config -m TCP_CONG_DCTCP
    $ ./scripts/config -m TCP_CONG_BBR2
    $ make -j$(nproc) LOCALVERSION=-prague-1
    $ sudo make install
    $ sudo make modules_install
    $ sudo update-grub

How to purge kernel when it is messed up?
.. code-block:: console
    $ dpkg --list | egrep -i --color 'linux-image|linux-headers' | grep prague
    $ sudo apt-get purge linux-image-5.10.31-3cc3851880a1-prague-37
    $ sudo apt purge linux-headers-5.10.31-3cc3851880a1-prague-37


FFmpeg related tutorial
=======================
https://stackoverflow.com/questions/56972903/how-to-read-mkv-bytes-as-video#:~:text=import%20imageio%20%23%20Get%20bytes%20of%20MKV%20video,first%20few%20bytes%20of%20content%20look%20like%20this%3A
https://stackoverflow.com/questions/63195747/how-to-specify-start-and-end-frames-when-making-a-video-with-ffmpeg
.. code-block:: console
    $ ffmpeg -i sample-5s.mp4 -start_number 10 -frames:v 30 -c:a copy -c:v vp9 -b:v 1M output.mkv
    $ pip3 install imageio
    $ with open('output.mkv', 'rb') as file: content = file.read()


Google WebRTC experiments
=========================

How to run the client on the same computer. (line 1 && line 3)
.. code-block:: console
    $ sudo ./main_google.sh
    $ cd samples && npm start
    $ chromium-browser --disable-webrtc-encryption http://100.71.102.33:8080/src/content/capture/video-contenthint/




SCReAM related experiments
==========================

1. Get the scream repository.
.. code-block:: console
    $ git clone https://github.com/EricssonResearch/scream.git
    $ cd scream
    $ cmake .
    $ make


2. Generate a network BW profile. 
The python script `network_profile_generator.py` does that and saves the profile in `profile.txt`.
.. code-block:: console
    $ python3 network_profile_generator.py


3. Finally, run `main.sh` with sudo access on the server computer. (1st line)
`main.sh` invokes the server with the network BW simulator internally. (2nd line)
Note: my server is 192.168.100.33 and client is 192.168.100.37; the port used is 8080.
Instantly invoke the client on the client machine with sudo access. (3rd line)
.. code-block:: console
    $ sudo ./main.sh
    $ scream/bin/scream_bw_test_tx -ect 1 -log scream/test.txt 192.168.100.37 8080 
    $ sudo sudo bin/scream_bw_test_rx 192.168.100.33 8080




Webcam server
=============

This example illustrates how to read frames from a webcam and send them
to a browser.

Running
-------

First install the required packages:

.. code-block:: console

    $ pip install aiohttp aiortc

When you start the example, it will create an HTTP server which you
can connect to from your browser:

.. code-block:: console

    $ python webcam.py
    $ chromium-browser --disable-webrtc-encryption
Ref: https://peter.sh/experiments/chromium-command-line-switches/#disable-webrtc-encryption
You can then browse to the following page with your browser:

http://127.0.0.1:8080

Once you click `Start` the server will send video from its webcam to the
browser.

Additional options
------------------

If you want to play a media file instead of using the webcam, run:

.. code-block:: console

   $ python webcam.py --play-from video.mp4

   $ python3 webcam.py --play-from ../../../server/sample-5s.mp4 --play-without-decoding --audio-codec audio/opus --video-codec video/H264 --verbose --host 127.0.0.1 --port 8080

Pre-encoded Opus audio
......................

If you want to play an OGG file containing Opus audio without decoding the frames, run:

.. code-block:: console

   $ python webcam.py --play-from audio.ogg --play-without-decoding --audio-codec audio/opus

You can generate an example of such a file using:

.. code-block:: console

   $ ffmpeg -f lavfi -i "sine=frequency=1000:duration=20" -codec:a libopus -f ogg audio.ogg

Pre-encoded H.264 video
.......................

If you want to play an MPEGTS file containing H.264 video without decoding the frames, run:

.. code-block:: console

   $ python webcam.py --play-from video.ts --play-without-decoding --video-codec video/H264

You can generate an example of such a file using:

.. code-block:: console

   $ ffmpeg -f lavfi -i testsrc=duration=20:size=640x480:rate=30 -pix_fmt yuv420p -codec:v libx264 -profile:v baseline -level 31 -f mpegts video.ts

Pre-encoded VP8 video
.....................

If you want to play a WebM file containing VP8 video without decoding the frames, run:

.. code-block:: console

   $ python webcam.py --play-from video.webm --play-without-decoding --video-codec video/VP8

You can generate an example of such a file using:

.. code-block:: console

   $ ffmpeg -f lavfi -i testsrc=duration=20:size=640x480:rate=30 -codec:v vp8 -f webm video.webm

Credits
-------

The original idea for the example was from Marios Balamatsias.

Support for playback without decoding was based on an example by Renan Prata.
