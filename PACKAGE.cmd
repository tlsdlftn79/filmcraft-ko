@echo off
setlocal EnableExtensions DisableDelayedExpansion
pushd "%~dp0" || exit /b 1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\build-win.ps1" -Mode Package
set "PACKAGE_RESULT=%ERRORLEVEL%"
popd
exit /b %PACKAGE_RESULT%
