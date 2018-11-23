@echo off
setlocal
pushd %~dp0

set "SCRIPT_PATH=OdysseyTools\OdysseyDependencies\OdysseyDependencies.py"

if not exist %SCRIPT_PATH%              goto :no_script
call python3 -c "import colorama"   ||  goto :python3_error
call python3 %SCRIPT_PATH% %*       ||  goto :script_error
goto :EOF

:no_script
echo Warning: OdysseyDependencies.py not found
goto :EOF

:python3_error
echo Error: could not find python3.
echo Make sure it is accessible from environment variables
echo Make sure required modules are installed
echo Check Odyssey Developper Documentation on python3 for Odyssey
goto :EOF

:script_error
echo Error: OdysseyDependencies.py, found errors
goto :EOF
