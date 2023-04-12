from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from typing import List

import mass_report
import search_report

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mount the StaticFiles instance to the desired path
app.mount("/static/css", StaticFiles(directory="static/css"), name="static_css")
app.mount("/static/js", StaticFiles(directory="static/js"), name="static_js")
app.mount("/snapshot", StaticFiles(directory="snapshot"), name="snapshot")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/mass_search", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("mass_search_report.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("search_report.html", {"request": request})

@app.get("/groupcode", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("groupcode.html", {"request": request})

@app.post("/submit")
async def search_form(markk: List[str] = Form([]), marke: List[str] = Form([]),
                      classno: List[int] = Form([]), group: List[str] = Form([]), name: List[str] = Form([])):


    #변수 그룹 정리
    marks = []
    for i in range(len(markk)):
        if markk[i] is not None:
            marks.append({"mark_kor": markk[i], "mark_eng": marke[i]})

    groups = []
    for i in range(len(classno)):
        if classno[i] != 0:
            groups.append({"class_no": classno[i], "group_code": group[i], "name": name[i]})

    search_report.search_report(marks, groups)
    

    return {"complete" }


@app.post("/mass_submit")
async def mass_search_form(markks: List[str], markes: List[str],
                      classnos: List[int], groups: List[str], names: List[str]):

    #변수 그룹 정리
    marks = []
    for i in range(len(markks)):
        if markks[i] is not None:
            marks.append({"mark_kor": markks[i], "mark_eng": markes[i]})

    groups = []
    for i in range(len(classnos)):
        if groups[i] is not None:
            groups.append({"class_no": classnos[i], "group_code": groups[i], "name": names[i]})

    mass_report.mass_report(marks, groups)

    return {"mark1": markks[0], "class1": classnos[0], "group1":groups[0] }



@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello 헬로 {name}"}



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)