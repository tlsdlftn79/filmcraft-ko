@echo off
setlocal EnableExtensions DisableDelayedExpansion
pushd "%~dp0" || exit /b 1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\build-installer.ps1" %*
set "INSTALL_RESULT=%ERRORLEVEL%"
popd
exit /b %INSTALL_RESULT%
