@echo off

rem Start Redis server
start "" "E:\softwares\Redis-x64-5.0.14.1\redis-server.exe" 

rem Start Celery worker
start cmd /k "cd E:\production\kasheehrms\kashee && E:\production\kasheehrms\myenv\Scripts\activate && celery -A kashee worker --pool=solo"

rem Start Flower
start cmd /k "cd E:\production\kasheehrms\kashee && E:\production\kasheehrms\myenv\Scripts\activate && celery -A kashee flower --port=5555"
