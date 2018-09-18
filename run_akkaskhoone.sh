#!/bin/bash
python manage.py migrate
python add_to_db.py &
sleep 2
python manage.py runserver 0.0.0.0:80