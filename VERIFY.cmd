@echo off
setlocal EnableExtensions DisableDelayedExpansion
pushd "%~dp0" || exit /b 1
where py.exe >nul 2>nul
if not errorlevel 1 (
    py -3 "scripts\verify_release.py" --dist "dist" --manifest "dist\FilmCraft_v0.6.0_Stable_RELEASE_MANIFEST.json"
) else (
    where python.exe >nul 2>nul
    if errorlevel 1 (
        echo [ERROR] Python 3 not found. Required for release verification.
        popd
        exit /b 1
    )
    python "scripts\verify_release.py" --dist "dist" --manifest "dist\FilmCraft_v0.6.0_Stable_RELEASE_MANIFEST.json"
)
set "VERIFY_RESULT=%ERRORLEVEL%"
popd
exit /b %VERIFY_RESULT%
