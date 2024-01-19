#!/bin/fish
set -lx PIPENV_PIPFILE /home/rodrigokimura/dev/project_money/Pipfile
cd /home/rodrigokimura/dev/project_money/ || exit
pipenv run gunicorn project_money.wsgi:application \
    --pythonpath src \
    --workers 5 \
    -b 0.0.0.0:8000 \
    --log-level INFO \
    --enable-stdio-inheritance \
    --capture-output \
    -t 30
