import sys
import subprocess
import time




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
    subprocess.Popen(cmd).wait()
    #Delete the file from Input folder
    #subprocess.Popen(['mv', tempout + line.strip('.mp4'), googleout + '/' + line.strip('.mp4')]).wait()
    subprocess.Popen(['rm', inpath + line]).wait()
    print('Removed from FTP')
    #Remove name from Queue
    with open("queue.txt") as f:
      lines = f.readlines()
    with open("queue.txt", "w") as f:
      f.writelines(lines[1:])
    print("Removed from Queue")
  else:
    with open("queue.txt", "w") as f:
      f.writelines(lines[1:])
    time.sleep(0.5)