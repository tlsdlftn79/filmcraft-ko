@echo off
setlocal EnableExtensions DisableDelayedExpansion
pushd "%~dp0" || exit /b 1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\build-win.ps1" -Mode Test
set "TEST_RESULT=%ERRORLEVEL%"
popd
exit /b %TEST_RESULT%
