from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .scanners.dep_parser import parse_requirements
from .scanners.typosquat import detect_typos
from .scanners.vuln_scan import scan_vulnerabilities
from .scanners.report import aggregate_report

app = FastAPI(title="Supply Chain Attack Simulator")
app.mount('/static', StaticFiles(directory='app/static'), name='static')
templates = Jinja2Templates(directory='app/templates')

@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('upload.html', {'request': request})

@app.post('/scan', response_class=HTMLResponse)
async def scan(request: Request, file: UploadFile):
    content = (await file.read()).decode('utf-8', errors='ignore')
    deps = parse_requirements(content)
    typo_findings = detect_typos([n for (n,_) in deps])
    vuln_findings = scan_vulnerabilities(deps)
    report = aggregate_report(deps, typo_findings, vuln_findings)
    return templates.TemplateResponse('report.html', {'request': request, 'report': report})

@app.post('/api/scan')
async def api_scan(file: UploadFile):
    content = (await file.read()).decode('utf-8', errors='ignore')
    deps = parse_requirements(content)
    typo_findings = detect_typos([n for (n,_) in deps])
    vuln_findings = scan_vulnerabilities(deps)
    report = aggregate_report(deps, typo_findings, vuln_findings)
    return JSONResponse(report)
