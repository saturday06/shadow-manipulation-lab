@echo off

echo start_ok > "%SML_START_OK_FILE_PATH%"

setlocal
:loop
tasklist /FI "PID eq %SML_WAIT_PID%" /NH /FO CSV | find """%SML_WAIT_PID%""" > nul
if not errorlevel 1 (
    timeout /t 1 >nul
    echo Waiting for %SML_WAIT_PID%
    goto :loop
)
endlocal

@echo on

"%SML_BLENDER_PATH%" --start-console "%SML_BLEND_FILE_PATH%" -- "%SML_EXTRA_ARG%" || echo Done
exit 0
