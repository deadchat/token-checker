@echo off
title Install

pip install pyfiglet pystyle requests colorama fake_useragent

echo py main.py > start.bat
call start.bat