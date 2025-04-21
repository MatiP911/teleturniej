@echo off
if exist ".\.venv" goto CallAndRun
python -m venv .venv
call .\.venv\Scripts\activate
call pip3 install customtkinter
goto Run

:CallAndRun
call .\.venv\Scripts\activate
:Run
python .\main.py

pause
