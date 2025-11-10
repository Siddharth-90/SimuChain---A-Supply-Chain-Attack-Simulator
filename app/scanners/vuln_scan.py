import json
import re
from pathlib import Path
from typing import List, Tuple, Dict

MOCK_PATH = Path(__file__).with_name("mock_vulns.json")

def version_satisfies(version_spec: str, version_str: str) -> bool:
    import re
    m = re.match(r'(==|>=|<=|>|<|~=|!=)?\s*([0-9]+(?:\.[0-9]+){0,2})', version_spec.strip())
    if not m or not version_str:
        return False
    op = m.group(1) or "=="
    target = m.group(2)
    def to_tuple(s):
        return tuple(int(x) for x in (s.split('.') + ['0','0'])[:3])
    vt = to_tuple(version_str.strip('=<>!~ '))
    tt = to_tuple(target)

    if op == "==": return vt == tt
    if op == ">=": return vt >= tt
    if op == "<=": return vt <= tt
    if op == ">":  return vt > tt
    if op == "<":  return vt < tt
    if op == "~=": return vt[0] == tt[0] and vt >= tt
    if op == "!=": return vt != tt
    return False

def scan_vulnerabilities(deps: List[Tuple[str, str]]) -> List[Dict]:
    data = json.loads(MOCK_PATH.read_text(encoding="utf-8"))
    findings = []
    for name, version in deps:
        short_ver = ""
        m = re.search(r'([0-9]+(?:\.[0-9]+){0,2})', version)
        if m:
            short_ver = m.group(1)
        if name in data and short_ver:
            for rule in data[name]:
                if version_satisfies(rule["spec"], short_ver):
                    findings.append({
                        "type": "VULN",
                        "package": name,
                        "version": short_ver,
                        "cve": rule["cve"],
                        "severity": rule["severity"],
                        "description": f"{name} {short_ver} matches {rule['spec']} (mock) → {rule['cve']}",
                        "fix": rule["fix"]
                    })
    return findings
