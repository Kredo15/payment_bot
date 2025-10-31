#!/bin/sh

alembic revision --autogenerate -m "init"
alembic upgrade head

exec python3 main.py