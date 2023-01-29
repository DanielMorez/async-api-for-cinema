#!/bin/bash

export FLASK_APP=wsgi_app
flask db upgrade
gunicorn -w 4 -b 0.0.0.0:5001 'app:app'