---

RecFilter2 - A SFW filter for videos based on [NudeNet](https://github.com/notAI-tech/NudeNet), it **removes** SFW sections of video.

---

## Explanation:

RecFilter2 does the following operations:
 - Generate sample images at pre-determined intervals for the whole video;
 - Submit those sample to the NudeNet classification API;
 - Parse the results for each image based on the wanted search parameters;
 - Generate ffmpeg commands to extract the NSFW sections;
 - Combine these sections in to a final video.

---

## Installation:

Download the files to a directory and enter `pip install -r requirements` to install the Python modules.

**NOTE:** It has been tested and developed using Python 3.7.9 - we know it works using this version.

RecFilter2.py is capable of being compiled using pyinstaller, `pyinstaller --onefile RecFilter2.py`

You can also use it as part of the post-processing for CTBRec, (not tested but the theory is sound ;) ), eg.
`python RecFilter2.py ${absolutePath} -m ${sanitizedModelName} -s ${sanitizedSiteName}`

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

Examples:

`python RecFilter2.py d:\captures\cb_freddo_20210202-181818.mp4`

Uses the default values: -i 60 -e 0 -b 0 -f 0

`python RecFilter2.py d:\captures\cb_freddo_20210202-181818.mp4 -i 45`

Sample image interval is 45 seconds, default values for everything else.

`python RecFilter2.py d:\captures\cb_freddo_20210202-181818.mp4 -b 420 -e 300`

Skip 420 seconds of video at the start and 300 seconds at the end, default values for everything else.

`python RecFilter2.py d:\captures\cb_freddo_20210202-181818.mp4 -m sexy_legs -s supacams`

Look for an entry in the configuration file for model `sexy_legs` on the site `supacams`, the values from the configuration file will override any given on the command line.



## Config file

**For the configuration file to be detected it has to have the same basename as the script/executable, (eg. `RecFilter2.json` if the script is named `RecFilter2.py`), and reside in the same directory as the script/executable.**

The configuration file is optional, without it RecFilter2 will use the default values for its parameters.

The file is in JSON format and contains optional parameters pertaining to particular models and the default body area search.

Example:
```
{
  "default": "EXPOSED_ANUS,EXPOSED_BELLY,EXPOSED_BREAST,EXPOSED_BUTTOCKS,EXPOSED_GENTALIA,EXPOSED_FEET,FACE",
  "models": [  
    {
      "name": "modelname",
      "site": "camsite",
      "interval": 45,
      "extension": 10,
      "search": "EXPOSED_BELLY",
      "begin": 330,
      "finish": 0
    },
    {
      "name": "modelname2",
      "site": "camsite3",
      "interval": 50,
      "extension": 5,
      "search": "EXPOSED_FEET",
      "begin": 0,
      "finish": 0
    }
  ]
}
```
The body areas searched for are set in the script to:
`EXPOSED_BREAST, EXPOSED_BUTTOCKS, EXPOSED_ANUS, EXPOSED_GENITALIA, EXPOSED_BELLY`

However, you can modify this by editing the `default` value in the configuration file.

**Model entries:**
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

