param(
  [string]$Repo = "D:\work\prj\tul"
)
$Tul = Join-Path $Repo "bin\tul"
python $Tul setup install $Repo
