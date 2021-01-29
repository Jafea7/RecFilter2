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

The search for body areas defaults to: 'EXPOSED_BREAST', 'EXPOSED_BUTTOCKS', 'EXPOSED_ANUS', 'EXPOSED_GENITALIA', 'EXPOSED_BELLY'

If you want something else then either:
 - edit the source;
 - create an entry in the config for particular models.

Examples:

`python RecFilter2.py d:\captures\cb_freddo_20210202-181818.mp4`

Uses the default values: -i 60 -e 0 -b 0 -f 0

`python RecFilter2.py d:\captures\cb_freddo_20210202-181818.mp4 -i 45`

Sample image interval is 45 seconds, default values for everything else.

`python RecFilter2.py d:\captures\cb_freddo_20210202-181818.mp4 -b 420 -e 300`

Skip 420 seconds of video at the start and 300 seconds at the end, default values for everything else.

`python RecFilter2.py d:\captures\cb_freddo_20210202-181818.mp4 -m sexy_legs -s supacams`

Look for an entry in the config file for model `sexy_legs` on the site `supacams`, the values from the config file will override any given on the command line.



## Config file

The configuration file is in JSON format and contains optional parameters pertaining to particular models.

The configuration file has to have the same basename as the script/executable, ie. RecFilter2.json for RecFilter2.py.

If you change the name of the script/executable then the configuration has to be changed also.

**The script/executable looks for the configuration file in the same directory as itself.**

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


The valid body areas to detect on are:
| class name          | Description |
|---------------------|-------------|
| EXPOSED_ANUS        | Exposed Anus; Any gender |
| EXPOSED_ARMPITS     | Exposed Armpits; Any gender |
| COVERED_BELLY       | Provocative, but covered Belly; Any gender |
| EXPOSED_BELLY       | Exposed Belly; Any gender |
| COVERED_BUTTOCKS    | Provocative, but covered Buttocks; Any gender |
| EXPOSED_BUTTOCKS    | Exposed Buttocks; Any gender |
| FACE_F              | Female Face |
| FACE_M              | Male Face |
| COVERED_FEET        | Covered Feet; Any gender |
| EXPOSED_FEET        | Exposed Feet; Any gender |
| COVERED_BREAST_F    | Provocative, but covered Breast; Female |
| EXPOSED_BREAST_F    | Exposed Breast; Female |
| COVERED_GENITALIA_F | Provocative, but covered Genitalia; Female |
| EXPOSED_GENITALIA_F | Exposed Genitalia; Female |
| EXPOSED_BREAST_M    | Exposed Breast; Male |
| EXPOSED_GENITALIA_M | Exposed Genitalia; Male |

The following are gender neutral, ie. they will match Male or Female:
| class name        | Description |
|-------------------|-------------|
| FACE              | Face; Any gender |
| EXPOSED_BREAST    | Exposed Breast; Any gender |
| EXPOSED_GENITALIA | Exposed Genitalia; Any gender |
