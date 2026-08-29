@echo off
cd /d "%~dp0"
echo Computing rubber duck return-time statistics for a=1.6...
python 204ducks 1.6
echo.
pause
