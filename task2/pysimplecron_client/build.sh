#!/bin/bash
source venv/bin/activate
pyinstaller --paths venv/lib/python3.8/site-packages --onefile cli.py -n pysimplecron