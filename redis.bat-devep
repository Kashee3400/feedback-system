@echo off

rem Start Redis server
start "" "K:\Softwares\Redis-x64-5.0.14.1\redis-server.exe" 

rem Start Celery worker
start cmd /k "cd K:\Django\inventory\invent && K:\Django\inventory\myenv\Scripts\activate && celery -A invent worker --pool=solo"

rem Start Flower
start cmd /k "cd K:\Django\inventory\invent && K:\Django\inventory\myenv\Scripts\activate && celery -A invent flower --port=5555"
