param(
    [string]$Repo = "D:\work\prj\tul"
)

$ErrorActionPreference = "Stop"
$Repo = (Resolve-Path $Repo).Path
$Tul = Join-Path $Repo "bin\tul"
$Bin = Join-Path $HOME "bin"
New-Item -ItemType Directory -Force -Path $Bin | Out-Null
$Launcher = Join-Path $Bin "tul.ps1"
@"
param([Parameter(ValueFromRemainingArguments=`$true)][string[]]`$Args)
python "$Tul" @Args
"@ | Set-Content -Encoding UTF8 -Path $Launcher

Write-Host "Installed tul launcher at $Launcher"
Write-Host "Next:"
Write-Host "  Set-Location $Repo"
Write-Host "  python $Tul status ."
