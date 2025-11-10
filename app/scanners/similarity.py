def levenshtein(a: str, b: str) -> int:
    a, b = a.lower(), b.lower()
    if a == b:
        return 0
    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        curr = [i]
        for j, cb in enumerate(b, start=1):
            ins = prev[j] + 1
            dele = curr[j-1] + 1
            sub = prev[j-1] + (0 if ca == cb else 1)
            curr.append(min(ins, dele, sub))
        prev = curr
    return prev[-1]

def similarity_score(a: str, b: str) -> float:
    if not a and not b:
        return 1.0
    dist = levenshtein(a, b)
    max_len = max(len(a), len(b))
    return 1.0 - (dist / max_len if max_len else 0.0)
