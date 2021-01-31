<#
  ./RF-Batch.ps1 <dir> [-interval <int>] [-extension <int>] [-begin <int>] [-finish <int>] [-model <model> -site <site>] [-keep]
#>

param (
  [Parameter(Mandatory=$true)][string]$dir,
  [Parameter(Mandatory=$false)][int]$interval = 60,
  [Parameter(Mandatory=$false)][int]$extension = 0,
  [Parameter(Mandatory=$false)][int]$begin = 0,
  [Parameter(Mandatory=$false)][int]$finish = 0,
  [Parameter(Mandatory=$false)][string]$model,
  [Parameter(Mandatory=$false)][string]$site,
  [Parameter(Mandatory=$false)][switch]$keep
)

$modsit = ""
if ($model -and $site) {
  $modsit = " -m $($model) -s $($site)"
}
$k = ''
if ($keep) {
  $k = ' -k'
}

$include = @("*.mp4","*.mkv","*.ts")
$files = (Get-ChildItem -Path "$($dir)/*" -Include $include)

foreach ($file in $files) {
  $pyArgs = "RecFilter2.py `"$($file.FullName)`" -i $($interval) -e $($extension) -b $($begin) -f $($finish)$($modsit)$($k)"
  Start-Process -FilePath python.exe -ArgumentList $pyArgs -Wait -NoNewWindow
}
