#!/bin/bash

#python -m venv .venv
#source .venv/bin/activate
#pip install --upgrade pip

uvicorn interface/result_flask:app --reload & pip install -r requirements.txt & scrapy crawl fix_price
