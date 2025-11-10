from typing import List, Dict
from .similarity import similarity_score

POPULAR = [
    "requests", "flask", "django", "numpy", "pandas", "scipy", "matplotlib",
    "fastapi", "uvicorn", "jinja2", "sqlalchemy", "pydantic", "pytest"
]

def detect_typos(deps: List[str], threshold: float = 0.82) -> List[Dict]:
    findings = []
    for name in deps:
        best = None
        best_score = 0.0
        for legit in POPULAR:
            score = similarity_score(name, legit)
            if score > best_score:
                best_score, best = score, legit
        if best and best != name and best_score >= threshold:
            findings.append({
                "type": "TYPO",
                "package": name,
                "looks_like": best,
                "score": round(best_score, 3),
                "severity": "HIGH" if best_score >= 0.9 else "MEDIUM",
                "description": f"Package '{name}' is similar to '{best}' (score={best_score:.3f})."
            })
    return findings
