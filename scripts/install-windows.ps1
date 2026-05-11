param(
  [string]$Repo = "D:\work\prj\tul",
  [string]$Dest = "D:\work\bin\tul.cmd",
  [string]$LibDest = "D:\work\home\.config\tul\lib"
)

$ErrorActionPreference = "Stop"

$Repo = (Resolve-Path $Repo).Path
Set-Location $Repo

python -m py_compile .\bin\tul
python -m py_compile (Get-ChildItem .\lib\tulcore -Filter "*.py" | ForEach-Object { $_.FullName })

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Dest) | Out-Null
New-Item -ItemType Directory -Force -Path $LibDest | Out-Null

$TulPath = Join-Path $Repo "bin\tul"
$Wrapper = "@echo off`r`npython `"$TulPath`" %*`r`n"
[System.IO.File]::WriteAllText($Dest, $Wrapper, [System.Text.UTF8Encoding]::new($false))

$TargetCore = Join-Path $LibDest "tulcore"
if (Test-Path $TargetCore) { Remove-Item $TargetCore -Recurse -Force }
Copy-Item -LiteralPath (Join-Path $Repo "lib\tulcore") -Destination $LibDest -Recurse -Force

Write-Host "Installed tul:"
Write-Host "  $Dest"
Write-Host "  $TargetCore"
