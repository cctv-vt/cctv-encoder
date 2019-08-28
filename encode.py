import sys
import ffmpy
import os
import json
import subprocess
import math
import logging


inpath = sys.argv[1]
filename = sys.argv[2]
outpathbase = sys.argv[3]
googleout = sys.argv[4]
googleuser = sys.argv[5]



fullname = filename.strip('.mp4')
year = fullname[-4:]
month = fullname[-8:-6]
day = fullname[-6:-4]
name = fullname[:-11]

logging.basicConfig(filename= 'cctv-encoder.log', filemode='a', level=logging.DEBUG, format='%(asctime)s:%(levelname)s: ' + fullname +': %(message)s')

outpath = outpathbase + '/' + fullname + '/'

os.makedirs(outpath,exist_ok=True)

#PROBE
probe = ffmpy.FFprobe(
  global_options={"-loglevel quiet"},
  inputs={ inpath+filename : "-print_format json -show_streams"}
).run(stdout= subprocess.PIPE)



probe_obj = json.loads(probe[0].decode('utf-8'))

logging.info(probe_obj)

#VIDEO
ff = ffmpy.FFmpeg(
  global_options={'-y -v quiet -stats'},
  inputs={ inpath+filename : None },
  outputs={ outpath + fullname + '.broadband.mp4': '-vf "scale=-2:720" -b:v 1M'}
)

try:
  logging.info("Begin Encode")
  ff.run()
except:
  logging.error('Failed to Encode Video')

#THUMBNAILS


rate = str(math.floor((float(probe_obj['streams'][0]['duration'])/10)))

thumb = ffmpy.FFmpeg(
 global_options={"-v quiet"},
 inputs={ inpath+filename : None },
 outputs={ outpath + fullname + '.%d.jpg' : ['-vf', 'scale=-2:540,fps=1/' + rate ], outpath + fullname + '.%d.tn.jpg' : ['-vf', 'fps=1/' + rate, '-s', '160x90' ]}
)
try:
  logging.debug('Begin Thumbnail Encode')
  thumb.run()
except:
  logging.error('Failed to create Thumbnails')


logging.info('Month: ' + month + ' Day: ' + day +  ' Year: ' + year + ' Filename: ' + name)
subprocess.Popen(['sudo', '-u', googleuser,'mkdir', '--parents',googleout + year + '/' + month + '/' + fullname ]).wait()
subprocess.Popen(['sudo', '-u', googleuser,'cp','-r', outpath , googleout + year + '/' + month + '/']).wait()
logging.info('Coppied to ' + googleout + year + '/' + month + '/' + fullname)