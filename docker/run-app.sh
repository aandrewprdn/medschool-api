#!/bin/bash

cd /code

poetry run uvicorn src.main:app --host 0.0.0.0 --port 3000 --reload