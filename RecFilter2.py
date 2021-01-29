# All the hard coding done by Demo, all the easy coding done by Jafea7 ;)
import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from nudenet import NudeDetector

detector = NudeDetector()

pushstack = []
def pushdir(dirname):
  global pushstack
  pushstack.append(os.getcwd())
  os.chdir(dirname)

def popdir():
  global pushstack
  os.chdir(pushstack.pop())

parser = argparse.ArgumentParser(prog='RecFilter', description='RecFilter: Remove SFW sections of videos')
parser.add_argument('file', type=str, help='Video file to process')
parser.add_argument('-i', '--interval', type=int, default=60, help='Interval between image samples (default: 60)')
parser.add_argument('-e', '--extension', type=int, default=0, help='Extend time prior to section start (default: 0)')
parser.add_argument('-m', '--model', type=str, help='Model name for config preset')
parser.add_argument('-s', '--site', type=str, help='Site that the model appears on')
parser.add_argument('-k', '--keep', action='store_true', help='Keep temporary working files (default: False)')

args = parser.parse_args()
if ((((args.model is not None) and 
    (args.site is None))) or
    ((args.site is not None) and
    (args.model is None))):
  parser.error('The -model argument requires a -site argument')

video_name = args.file
frame_duration = args.interval
frame_extension = args.extension
model = args.model
site = args.site
keep = args.keep

# Default checkinglist is gender neutral, if a particular gender is required it can be entered into the config file per model
# EXPOSED_BREAST_F EXPOSED_GENITALIA_F EXPOSED_BREAST_M EXPOSED_GENITALIA_M 
checkinglist = ['EXPOSED_BREAST', 'EXPOSED_BUTTOCKS', 'EXPOSED_ANUS', 'EXPOSED_GENITALIA', 'EXPOSED_BELLY']

if ((model is not None) and (site is not None)):
  config_path = os.path.abspath(sys.argv[0]).rsplit('.', 1)[0] + '.json'
  found = False
  try:
    with open(config_path) as f:
      data = json.load(f)
      for cammodel in data:
        if (cammodel['name'].lower() == model):
          if (cammodel['site'].lower() == site):
            frame_duration = cammodel['interval']
            frame_extension = cammodel['extension']
            checkinglist = cammodel['search'].split(',')
            found = True
            break
      if not found:
        print(model + ' at ' + site + ' not found, using defaults.')
  except:
    print('No config file \'%s\' found, using defaults.' % config_path)

imagelist = []
lines = []
beginnings = []
endings = []

i = 0
b = 0
e = 0
p = 0
z = 0

video_path = os.path.abspath(video_name) # Get the full video path
pushdir(Path(video_path).parent) # Change to video container directory

tmpdir = '~' + Path(video_name).stem
try:
  os.mkdir(tmpdir)
  pushdir(tmpdir) # Change to temporary directory
  print('Created temporary directory')
except OSError:
  sys.exit('Creation of the temporary directory failed')

os.system('ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i ' + video_path + ' > tmp')
duration = int(float(open('tmp', 'r').read().strip()))

print('Creating sample images')
for interval in range(1, duration, frame_duration):
  os.system('ffmpeg -v quiet -y -skip_frame nokey -ss ' + str(interval) + ' -i ' + video_path + ' -vf select="eq(pict_type\\,I),scale=800:-1" -vframes 1 image-' + str(interval).zfill(7) + '.jpg')

print('Analysing images')
with open('API-Results.txt',"w") as outfile:
  for filename in os.listdir(os.getcwd()):
    if filename.endswith(".jpg"):
      output  = detector.detect(filename)
      y = 0
      stringoutput = ''
  
      while y < len(output):
        match = re.search(r'\b[A-Z].*?\b', str(output[y]))
        #print(match.group())
        stringoutput += str(match.group()) + '  '
    
        y +=1
      outfile.write(filename + '    ' + stringoutput + '\n')
      #print(stringoutput)

with open('API-Results.txt',"r") as infile, open('output.txt',"w") as outfile:
  for line in infile:
    for check in checkinglist:
      if check in line:
        #print(line) 
        outfile.write(line)
        break


with open('output.txt',"r") as infile, open('list.txt',"w") as outfile:
  for line in infile:
    match = re.search(r'\d\d\d\d\d\d\d', line)
    x = int(match.group())
    imagelist.append(x)
    lines.append(line)
  #print(imagelist)
  
  while i < len(imagelist):
    if i == 0: #if first element of imagelist
      if len(imagelist) == 1 or imagelist[i+1] - imagelist[i] > frame_duration: #if no segment within frame_durations
        beginnings.append(imagelist[i]) 
        endings.append(imagelist[i] + frame_duration) #become your own frame_durations segment
      else: 
        b = imagelist[i] #else become beginning of multi-minute-segment
        if e > b:
          beginnings.append(b)
          endings.append(e)

    elif i == len(imagelist)-1: #if last element if imagelist
      if imagelist[i] - imagelist[i-1] > frame_duration: #if no segment within frame_durations
        beginnings.append(imagelist[i] - frame_extension) 
        endings.append(imagelist[i] + frame_duration) #become your own frame_durations segment
      else:
        e = imagelist[i] #else become ending of multi-minute-segment
        if e > b:
          beginnings.append(b)
          endings.append(e)

    elif imagelist[i+1] - imagelist[i] > frame_duration and imagelist[i] - imagelist[i-1] > frame_duration: #lone wolf segment example: if model flashes breasts on contactsheet frame
      beginnings.append(imagelist[i] - frame_extension) 
      endings.append(imagelist[i] + frame_duration) #become your own frame_durations segment

    elif imagelist[i+1] - imagelist[i] > frame_duration: #multi-minute ending segment
      e = imagelist[i] + frame_duration
      if e > b:
        beginnings.append(b)
        endings.append(e)

    elif imagelist[i] - imagelist[i-1] > frame_duration: #multi-minute beginning segment
      b = imagelist[i] - frame_extension
      if e > b:
        beginnings.append(b)
        endings.append(e)
    i += 1
      
  #print(beginnings)
  #print(endings)

  print('Creating video segments')
  while p < len(beginnings):
    duration = endings[p] - beginnings[p]
    outfile.write('file ' + '\'out' + str(p) + '.mp4\'' + '\n')
#    print('ffmpeg -v quiet -stats -vsync 0 -ss ' + str(beginnings[p]) + ' -i ' + video_path + ' -t ' + str(duration) + ' -c copy out' + str(p) + '.mp4')
    os.system('ffmpeg -v quiet -stats -vsync 0 -ss ' + str(beginnings[p]) + ' -i ' + video_path + ' -t ' + str(duration) + ' -c copy out' + str(p) + '.mp4')
    p += 1

print('Creating final video')
os.system('ffmpeg -v quiet -stats -y -vsync 0 -safe 0 -f concat -i list.txt -c copy "' + video_path.rsplit('.', 1)[0] + '-Compilation' + str(frame_duration) + '-' + str(frame_extension) + '.mp4"')

popdir() # Return to temporary directory parent
if (not keep): # Delete the temporary directory if argv[4] = false
  print('Deleting temporary files')
  shutil.rmtree(tmpdir, ignore_errors=True)

popdir() # Return to initial directory
