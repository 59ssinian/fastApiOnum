#!/bin/bash
pgrep -f "python -m uvicorn main:app" | xargs kill
echo "The application has stopped."
