#!/bin/bash

sleep 5

uvicorn app.api.server:app --reload --workers 1 --host 0.0.0.0 --port 8000 &

sleep 15

alembic upgrade head

echo "The migrations migrated"

sleep infinity