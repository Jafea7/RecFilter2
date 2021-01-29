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
| -i        | Interval in seconds between each generated sample image used for analysis, (Default is 60). |
| -e        | Number of seconds to include prior to each selected video section, (Default is 0). |
| -b        | Number of seconds to skip at the beginning of the video, eg. in the event of a 'highlights' video being shown, (Default is 0). |
| -f        | Number of seconds to skip at the end of the video, eg. in the event of a 'highlights' video being shown, (Default is 0). |
| -m        | Model name to match in the config file, site (-s) parameter must also be supplied, (Default is none). |
| -s        | Site name to match in the config file, (Default is none). |
| -k        | Keep the temporary work directory and its contents, (Default is false). |

## Config file

The configuration file is in JSON format and contains optional parameters pertaining to particular models.

Example:
```
[
  {
    "name": "modelname",
    "site": "camsite",
    "interval": 45,
    "extension": 10,
    "search": "EXPOSED_BELLY",
    "begin": 330,
    "finish": 0
  }
]
```
| Parameter | Description |
|-----------|-------------|
| name      | Name of the model. |
| site      | Name of the cam site. |
| interval  | Interval in seconds between each generated sample image used for analysis. |
| extension | Number of seconds to include prior to each selected video section. |
| search    | Body areas to analyse images for, covered or exposed. (More info below.) |
| begin     | Number of seconds to skip at the beginning of the video, eg. in the event of a 'highlights' video being shown. |
| finish    | Number of seconds to skip at the end of the video, eg. in the event of a 'highlights' video being shown. |

