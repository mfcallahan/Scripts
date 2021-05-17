@echo off
set size=0
for /r %%x in (folder\*) do set /a size+=%%~zx
echo %size% Bytes
Pause