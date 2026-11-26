@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 zensus_download.py
  goto :ende
)
where python >nul 2>nul
if %errorlevel%==0 (
  python zensus_download.py
  goto :ende
)
echo Python wurde nicht gefunden.
echo Bitte von https://www.python.org/downloads/ installieren.
echo Bei der Installation "Add Python to PATH" ankreuzen. Danach diese Datei erneut starten.
pause
:ende
