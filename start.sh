#!/bin/bash

# Starta kgsarchive.py i bakgrunden
python3 kgsarchive.py &

# Starta gunicorn för flask-applikationen
gunicorn app:app
