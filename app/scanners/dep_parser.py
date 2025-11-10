from typing import List, Tuple

def parse_requirements(content: str) -> List[Tuple[str, str]]:
    deps = []
    for raw in content.splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        name = line
        version = ""
        for sep in ["==", ">=", "<=", ">", "<", "~=", "!="]:
            if sep in line:
                name, version = line.split(sep, 1)
                name = name.strip()
                version = sep + version.strip()
                break
        deps.append((name.replace('_','-'), version))
    return deps
