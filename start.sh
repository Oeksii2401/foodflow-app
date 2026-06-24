#!/bin/bash
env $(cat /workspaces/foodflow-app/.env | grep -v '^#' | grep -v '^$' | sed 's/ *#.*//' | tr '\n' ' ') python -m uvicorn main:app --reload
