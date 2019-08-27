import sys
import subprocess
import time
import logging


logging.basicConfig(filename= 'cctv-encoder.log', filemode='a', level=logging.DEBUG, format='%(asctime)s:%(levelname)s: %(message)s')

try:
  inpath = sys.argv[1]
except:
  inpath = "/home/gobolin/Videos/VideoInput/"

try:
  tempout = sys.argv[2]
except:
  tempout = "/home/gobolin/Videos/VideoOutput/"

googleout = sys.argv[3]

googleuser = sys.argv[4]

while True:
  with open("queue.txt") as f:
    lines = f.readlines()
  if lines:
    line = lines[0].strip('\n')
    #print(line)
    cmd = ['python3', 'encode.py', inpath, line, tempout, googleout, googleuser]
    #Run the Encoder
    logging.info('Now encoding ' + line)
    try:
      subprocess.Popen(cmd).wait()
      logging.debug('Finished encoding')
    except:
      logging.error('Could not encode')

    #Delete the file from Input folder
    #subprocess.Popen(['mv', tempout + line.strip('.mp4'), googleout + '/' + line.strip('.mp4')]).wait()
    logging.info('Removing ' + line + ' from ' + inpath)
    try:
      subprocess.Popen(['rm', inpath + line]).wait()
      logging.debug('Removed')
    except:
      logging.error('Could not Remove')

    #Remove name from Queue
    with open("queue.txt") as f:
      lines = f.readlines()
    logging.info('Removing ' + line + ' from Queue')
    try:
      with open("queue.txt", "w") as f:
        f.writelines(lines[1:])
        logging.debug('Removed')
    except:
        logging.debug('Could not remove')

  else:
    with open("queue.txt", "w") as f:
      f.writelines(lines[1:])
    time.sleep(0.5)