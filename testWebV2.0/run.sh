#!/bin/bash
source env/bin/activate
gunicorn -w 3 -b 0.0.0.0:8000 app:app
