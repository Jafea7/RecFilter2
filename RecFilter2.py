#!/usr/bin/python
import argparse
import json
import os
import re
import shutil
import signal
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

def exit_handler(signum, frame):
  if video_path is not None: # Haven't got this then have only read config
    if tmpdir is not None:   # If we got this then we're in the video or tmpdir
      if Path(os.getcwd()).stem == tmpdir: # If in the tmpdir then retrace a dir
        popdir()
      shutil.rmtree(tmpdir, ignore_errors = True) # Nuke the tmpdir
  sys.exit(0)

signal.signal(signal.SIGINT, exit_handler) # Handle Ctrl-C

print('\n--- RecFilter2 ---')
parser = argparse.ArgumentParser(prog='RecFilter', description='RecFilter: Remove SFW sections of videos')
parser.add_argument('file', type=str, help='Video file to process')
parser.add_argument('-i', '--interval', type=int, default=60, help='Interval between image samples (default: 60)')
parser.add_argument('-e', '--extension', type=int, default=0, help='Extend time prior to section start (default: 0)')
parser.add_argument('-b', '--beginning', type=int, default=1, help='Skip x seconds of beginning (default: 1)')
parser.add_argument('-f', '--finish', type=int, default=0, help='Skip x seconds of finish (default: 0)')
parser.add_argument('-m', '--model', type=str, help='Model name for config preset')
parser.add_argument('-s', '--site', type=str, help='Site that the model appears on')
parser.add_argument('-k', '--keep', action='store_true', help='Keep temporary working files (default: False)')
parser.add_argument('-v', '--verbose', action='store_true', help='Output working information (default: False)')

args = parser.parse_args()
if ((((args.model is not None) and 
    (args.site is None))) or
    ((args.site is not None) and
    (args.model is None))):
  parser.error('The -model argument requires a -site argument')

video_name = args.file
frame_duration = args.interval
frame_extension = args.extension
skip_begin = args.beginning
skip_finish = args.finish
if args.model is not None:
  model = args.model.lower()
else:
  model = None
if args.site is not None:
  site = args.site.lower()
else:
  site = None
keep = args.keep
verbose = args.verbose

config_path = os.path.abspath(sys.argv[0]).rsplit('.', 1)[0] + '.json'
try:
  with open(config_path) as f:
    data = json.load(f)
    config = True
except:
  print('INFO: No config file \'%s\' found.' % config_path)
  config = False

# Default checkinglist is gender neutral, if a particular gender is required it can be entered into the config file per model
# Other terms can also be set in the config, see https://github.com/Jafea7/RecFilter2 for valid terms
checkinglist = ['EXPOSED_BREAST', 'EXPOSED_BUTTOCKS', 'EXPOSED_ANUS', 'EXPOSED_GENITALIA', 'EXPOSED_BELLY']

if config:
  if 'default' in data:
    if str(data['default']) != "":
      checkinglist = data['default'].split(',')
  if ((model is not None) and (site is not None)):
    found = False
    for cammodel in data['models']:
      if (cammodel['name'].lower() == model):
        if (cammodel['site'].lower() == site):
          frame_duration = cammodel['interval']
          frame_extension = cammodel['extension']
          checkinglist = cammodel['search'].split(',')
          skip_begin = cammodel['begin']
          skip_finish = cammodel['finish']
          found = True
          break
    if not found:
      print('INFO: \'' + model + '\' at \'' + site + '\' not found, using defaults.')

print('INFO: -i ' + str(frame_duration) + ' -e ' + str(frame_extension) + ' -b ' + str(skip_begin) + ' -f ' + str(skip_finish))
print('      ' + str(checkinglist))

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
  print('INFO: Created temporary directory')
except OSError:
  sys.exit('Creation of the temporary directory failed')

os.system('ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i "' + video_path + '" > tmp')
duration = int(float(open('tmp', 'r').read().strip())) - skip_finish
if verbose: print('Duration: ' + str(duration))

print('INFO: Creating sample images')
for interval in range(skip_begin, duration, frame_duration):
  os.system('ffmpeg -v quiet -y -skip_frame nokey -ss ' + str(interval) + ' -i "' + video_path + '" -vf select="eq(pict_type\\,I),scale=800:-1" -an -q:v 3 -vframes 1 image-' + str(interval).zfill(7) + '.bmp')
if skip_finish < 1:
  os.system('ffmpeg -v quiet -y -skip_frame nokey -ss ' + str(duration - 1) + ' -i "' + video_path + '" -vf select="eq(pict_type\\,I),scale=800:-1" -an -q:v 3 -vframes 1 image-' + str(duration - 1).zfill(7) + '.bmp')

print('INFO: Analysing images')
with open('API-Results.txt',"w") as outfile:
  for filename in os.listdir(os.getcwd()):
    if filename.endswith(".bmp"):
      output  = detector.detect(filename)
      y = 0
      stringoutput = ''
  
      while y < len(output):
        match = re.search(r'\b[A-Z].*?\b', str(output[y]))
        stringoutput += str(match.group()) + '  '
    
        y +=1
      outfile.write(filename + '    ' + stringoutput + '\n')
      if verbose: print(filename + ' - ' + stringoutput)

with open('API-Results.txt',"r") as infile, open('output.txt',"w") as outfile:
  for line in infile:
    for check in checkinglist:
      if check in line:
        outfile.write(line)
        break


with open('output.txt',"r") as infile, open('list.txt',"w") as outfile:
  for line in infile:
    match = re.search(r'\d\d\d\d\d\d\d', line)
    x = int(match.group())
    imagelist.append(x)
    lines.append(line)
#    if verbose: print(imagelist)
  
  while i < len(imagelist):
    if i == 0: #if first element of imagelist
      if len(imagelist) == 1 or imagelist[i + 1] - imagelist[i] > frame_duration: #if no segment within frame_durations
        beginnings.append(imagelist[i]) 
        endings.append(imagelist[i] + frame_duration) #become your own frame_durations segment
      else: 
        b = imagelist[i] #else become beginning of multi-minute-segment
        if e > b:
          beginnings.append(b)
          endings.append(e)

    elif i == len(imagelist) - 1: #if last element if imagelist
      if imagelist[i] - imagelist[i - 1] > frame_duration: #if no segment within frame_durations
        beginnings.append(imagelist[i] - frame_extension) 
        endings.append(imagelist[i] + frame_duration) #become your own frame_durations segment
      else:
        e = imagelist[i] #else become ending of multi-minute-segment
        if e > b:
          beginnings.append(b)
          endings.append(e)

    elif imagelist[i + 1] - imagelist[i] > frame_duration and imagelist[i] - imagelist[i - 1] > frame_duration: #lone wolf segment example: if model flashes breasts on contactsheet frame
      beginnings.append(imagelist[i] - frame_extension) 
      endings.append(imagelist[i] + frame_duration) #become your own frame_durations segment

    elif imagelist[i + 1] - imagelist[i] > frame_duration: #multi-minute ending segment
      e = imagelist[i] + frame_duration
      if e > b:
        beginnings.append(b)
        endings.append(e)

    elif imagelist[i] - imagelist[i - 1] > frame_duration: #multi-minute beginning segment
      b = imagelist[i] - frame_extension
      if e > b:
        beginnings.append(b)
        endings.append(e)
    i += 1
      
  if verbose: print('Image list: ' + str(imagelist) + '\nBeginnings: ' + str(beginnings) + '\nEndings: ' + str(endings))

  print('INFO: Creating video segments')
  while p < len(beginnings):
    duration = endings[p] - beginnings[p]
    outfile.write('file ' + '\'out' + str(p) + '.mp4\'' + '\n')
    if verbose: print('ffmpeg -v quiet -vsync 0 -ss ' + str(beginnings[p]) + ' -i "' + video_path + '" -t ' + str(duration) + ' -c copy out' + str(p) + '.mp4')
    os.system('ffmpeg -v quiet -vsync 0 -ss ' + str(beginnings[p]) + ' -i "' + video_path + '" -t ' + str(duration) + ' -c copy out' + str(p) + '.mp4')
    p += 1

print('INFO: Creating final video')
if verbose: print('ffmpeg -v quiet -y -vsync 0 -safe 0 -f concat -i list.txt -c copy "' + video_path.rsplit('.', 1)[0] + '-Compilation' + str(frame_duration) + '-' + str(frame_extension) + '.mp4"')
os.system('ffmpeg -v quiet -y -vsync 0 -safe 0 -f concat -i list.txt -c copy "' + video_path.rsplit('.', 1)[0] + '-Compilation' + str(frame_duration) + '-' + str(frame_extension) + '.mp4"')

popdir() # Return to temporary directory parent
if (not keep): # Delete the temporary directory if argv[4] = false
  print('INFO: Deleting temporary files')
  shutil.rmtree(tmpdir, ignore_errors=True)

popdir() # Return to initial directory
print('--- Finished ---\n')
