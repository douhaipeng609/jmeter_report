# -*- coding: utf-8 -*-
# @Time : 2020-07-05 19:40
# @Author : Hunk
# @File : main.py

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from module import *
from starlette.requests import Request

from starlette.templating import Jinja2Templates
app = FastAPI()
@app.get("/jmeter_report")
async def read_item(request: Request):
    templates = Jinja2Templates(
        directory="/Users/dhp/Documents/j_NEW/templates")
    # app.mount('/jmeter', StaticFiles(directory='jmeter_re'), name='jmeter_re')
    app.mount(
        '/',
        StaticFiles(
            directory='/Users/dhp/Documents/j_NEW/static'),
        name='static')
    return templates.TemplateResponse('index.html', {"request": request})


if __name__ == '__main__':
    import os

    os.system('uvicorn main:app --reload')
