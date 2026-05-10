param(
  [string]$Repo = "D:\work\prj\tul",
  [string]$Dest = "D:\work\bin\tul"
)

$ErrorActionPreference = "Stop"

$Repo = (Resolve-Path $Repo).Path
$Source = Join-Path $Repo "bin\tul"

if (!(Test-Path $Source)) {
  Write-Error "missing $Source"
  exit 1
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Dest) | Out-Null

$Wrapper = @"
@echo off
python "$Source" %*
"@

[System.IO.File]::WriteAllText($Dest + ".cmd", $Wrapper, [System.Text.UTF8Encoding]::new($false))

Write-Host "Installed Windows wrapper:"
Write-Host "  $Dest.cmd"
Write-Host ""
Write-Host "Ensure D:\work\bin is on PATH, then run:"
Write-Host "  tul status D:\work\prj\tul"
