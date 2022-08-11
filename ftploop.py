#python3 script to sftp file
#################################
#intended for test clients with 'ftp' test role
#communicated by Dr. Edward Grinshpun
#Example: python3 ftploop.py arghya password 192.168.18.34 /home/arghya/webrtc-demo/ToS-4k-1920.mov
#################################
iversion='1.2'
###

import logging
import pysftp
import os, sys
from datetime import datetime
import argparse
import sys

if (len(sys.argv) != 5):
	sys.exit("Usage: python3 ftploop.py <username> <password> <IP> <filepath+filename>")


USER = sys.argv[1]
PWD = sys.argv[2]

def setlog(log_):
        if log_=='DEBUG':
                lg=logging.DEBUG
        elif log_=='INFO':
                lg=logging.INFO
        elif log_=='ERROR':
                lg=logging.ERROR
        else:
                lg=logging.INFO
        for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)
        #set logging
        logging.basicConfig(format='%(asctime)s.%(msecs)03d %(module)s %(message)s', level=lg, datefmt='%H:%M:%S')


def printProgress(x,y):
    global time0
    global x0
    epoch_time=datetime.now().timestamp()
    elapsed_time=epoch_time-time0
    tputK=0.0
    if elapsed_time>=1.0:
        tput_bytes=x-x0
        x0=x 
        time0=epoch_time
        tputK=(float(tput_bytes)/(elapsed_time*1000))
        logging.info('tput-Kbytes {:>10.3f} dowload-percent {:>5.3f}\n'.format(float(tputK),100*float(x)/float(y)))

def clean(file):
    if os.path.exists(file):
        os.remove(file)
        logging.info(" removed old file "+file)
    else:
        logging.info("No local file "+file)

if __name__=='__main__':
    SERVER = sys.argv[3]
    file = sys.argv[4]
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys=None
    #parser=argparse.ArgumentParser()
    #parser.add_argument("--file", help="filename, deafault tears.tar")
    #parser.add_argument("--server", help="server, default 135.112.62.175 ")
    log='INFO'
    #parser.add_argument('--log', help='One of DEBUG, INFO, ERROR, default '+log)
    #args=parser.parse_args()
    #if args.file:
    #    file=args.file
    #if args.server:
    #    SERVER=args.server
    #if args.log:
    #    log=args.log
    setlog(log)
    logging.info("ftploop.py version "+iversion)
    try:
        while True:
            with pysftp.Connection(SERVER, username=USER, password=PWD, private_key=".ppk", cnopts=cnopts) as sftp:
                count=0
                clean(file)
                count=count+1
                x0=0
                try: 
                    time0=datetime.now().timestamp()   
                    sftp.get(file, localpath=file, callback=lambda x,y:printProgress(x,y))
                except KeyboardInterrupt:
                    logging.info("\n Exiting")
                    clean(file)
                    sys.exit()
                logging.info(" Got "+file+ " "+ str(count))
    except Exception as ex:
            logging.info("Exception ", ex)
            #continue


