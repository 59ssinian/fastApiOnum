#!/bin/bash
nohup /home/ubuntu/.virtualenvs/fastApiOnum/bin/python /home/ubuntu/main.py -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo "The application has started."
