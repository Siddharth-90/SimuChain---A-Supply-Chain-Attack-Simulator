import sys, json
from app.scanners.dep_parser import parse_requirements
from app.scanners.typosquat import detect_typos
from app.scanners.vuln_scan import scan_vulnerabilities
from app.scanners.report import aggregate_report

def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <requirements.txt>")
        sys.exit(1)
    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    deps = parse_requirements(content)
    typo_findings = detect_typos([n for (n,_) in deps])
    vuln_findings = scan_vulnerabilities(deps)
    report = aggregate_report(deps, typo_findings, vuln_findings)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
