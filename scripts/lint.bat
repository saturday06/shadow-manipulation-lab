setlocal
setlocal enabledelayedexpansion
pushd "%~dp0.."
set PYTHONUTF8=1
for /f "tokens=* usebackq" %%f in (`git ls-files "*.py"`) do ( set py_files=!py_files! %%f )
for /f "tokens=* usebackq" %%f in (`git ls-files "*.pyi"`) do ( set pyi_files=!pyi_files! %%f )
call poetry run mypy --show-error-codes %py_files% %pyi_files%
echo on
call poetry run flake8 --count --show-source --statistics %py_files% %pyi_files%
echo on
call poetry run pylint %py_files%
echo on
popd
endlocal
endlocal
pause
