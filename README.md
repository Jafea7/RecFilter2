---

RecFilter2 - A SFW filter for videos based on NudeNet, it **removes** SFW sections of video.

---

## Usage:

```
Python RecFilter2.py file \
       [-i <VALUE>] \
       [-e <VALUE>] \
       [-b <VALUE>] \
       [-f <VALUE>] \
       [-m <NAME>] \
       [-s <NAME>] \
       [-k]
```
| Parameter | Description |
|-----------|-------------|
| -i        | Interval in seconds between each generated sample image used for analysis, default is 60. |
| -e        | Number of seconds to include prior to each selected video section, default is 0. |
| -b        | Number of seconds to skip at the beginning of the video, eg. in the event of a 'highlights' video being shown, default is 0. |
| -f        | Number of seconds to skip at the end of the video, eg. in the event of a 'highlights' video being shown, default is 0. |
| -m        | Model name to match in the config file, site (-s) parameter must also be supplied, default is none. |
| -s        | Site name to match in the config file, default is none. |
| -k        | Keep the temporary work directory and its contents, default is false. |
