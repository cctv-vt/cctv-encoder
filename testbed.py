import ffmpy
import subprocess
import json
import math

probe = ffmpy.FFprobe(
  global_options={"-loglevel quiet"},
  inputs={"/home/gobolin/Videos/EncoderTesting/TestFileArchival.mp4" : "-print_format json -show_streams"}
).run(stdout= subprocess.PIPE)

probe_obj = json.loads(probe[0].decode('utf-8'))

rate = str(math.floor((float(probe_obj['streams'][0]['duration'])/10)))
print(rate)
thumb = ffmpy.FFmpeg(
  global_options={"-v quiet"},
  inputs={"/home/gobolin/Videos/EncoderTesting/TestFileArchival.mp4" : None },
  outputs={"images/thumbnail.%d.png" : ['-vf', 'fps=1/' + rate ], "images/thumbnail.%d.tn.png" : ['-vf', 'fps=1/' + rate, '-s', '160x90' ]}
)

thumb.run()