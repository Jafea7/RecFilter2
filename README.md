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
