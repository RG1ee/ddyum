#!/bin/bash

alembic upgrade head

if [ "$APP_MODE" = "DEV" ]; then
  uvicorn src.main:app --reload --workers 4 --host 0.0.0.0 --port 8000
else
  uvicorn src.main:app --proxy-headers --host ${PROD_HOST} --port ${PROD_PORT}
fi
"$@"
