import sys
import ffmpy
import os
import json
import subprocess
import math

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

outpath = outpathbase + '/' + fullname + '/'

os.makedirs(outpath,exist_ok=True)


#VIDEO
ff = ffmpy.FFmpeg(
  global_options={'-y -v quiet -stats'},
  inputs={ inpath+filename : None },
  outputs={ outpath + fullname + '.broadband.mp4': '-vf "scale=-2:720" -b:v 1M'}
)
ff.run()


#THUMBNAILS
probe = ffmpy.FFprobe(
  global_options={"-loglevel quiet"},
  inputs={ inpath+filename : "-print_format json -show_streams"}
).run(stdout= subprocess.PIPE)

probe_obj = json.loads(probe[0].decode('utf-8'))

rate = str(math.floor((float(probe_obj['streams'][0]['duration'])/10)))
print(rate)
thumb = ffmpy.FFmpeg(
 global_options={"-v quiet"},
 inputs={ inpath+filename : None },
 outputs={ outpath + fullname + '.%d.jpg' : ['-vf', 'scale=-2:540,fps=1/' + rate ], outpath + fullname + '.%d.tn.jpg' : ['-vf', 'fps=1/' + rate, '-s', '160x90' ]}
)

thumb.run()


print('Month: ' + month)
print('Day: ' + day)
print('Year: ' + year)
print('Filename: ' + name)
subprocess.Popen(['sudo', '-u', googleuser,'mkdir', '--parents',googleout + year + '/' + month + '/' + fullname ]).wait()
subprocess.Popen(['sudo', '-u', googleuser,'cp','-r', outpath , googleout + year + '/' + month + '/']).wait()
print('Coppied to google bucket')