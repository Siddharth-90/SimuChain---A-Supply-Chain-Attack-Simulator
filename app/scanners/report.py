from typing import List, Dict, Tuple

def aggregate_report(
    deps: List[Tuple[str,str]],
    typo_findings: List[Dict],
    vuln_findings: List[Dict]
) -> Dict:
    base = 0
    sev_map = {"LOW":1, "MEDIUM":3, "HIGH":5}
    for f in typo_findings + vuln_findings:
        base += sev_map.get(f.get("severity","LOW"),1)
    risk = "LOW"
    if base >= 8: risk = "HIGH"
    elif base >= 4: risk = "MEDIUM"
    return {
        "dependencies": [{"name": n, "version": v} for (n,v) in deps],
        "findings": typo_findings + vuln_findings,
        "risk_score": base,
        "risk_level": risk
    }
