Rem First check that all dependencies are installed
set installing=Installing python dependencies
echo %installing%
start /wait dependencies_win.bat

Rem Build app
set building=Building app
echo %building%
pyinstaller run.spec

Rem Move generated exe to EXES folder and remove temporal files
copy dist\dongle-app.exe EXES\win\

del /s /f /q build\*.*
for /f %%f in ('dir /ad /b build\') do rd /s /q build\%%f
rd build

del /s /f /q dist\*.*
for /f %%f in ('dir /ad /b dist\') do rd /s /q dist\%%f
rd dist

Rem Update github release