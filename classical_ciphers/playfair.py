def _prepare_key(key: str, alphabet: str):
    key = key.upper().replace("J", "I")
    seen = set()
    matrix = []

    for ch in key + alphabet:
        if ch == "J":
            ch = "I"
        if ch.isalpha() and ch not in seen:
            seen.add(ch)
            matrix.append(ch)

    return [matrix[i:i+5] for i in range(0, 25, 5)]


def _find(matrix, ch):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == ch:
                return r, c


def _prepare_text(text: str):
    text = text.upper().replace("J", "I")
    out = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else "X"
        if a == b:
            out.extend([a, "X"])
            i += 1
        else:
            out.extend([a, b])
            i += 2
    if len(out) % 2:
        out.append("X")
    return out


def encrypt(text: str, key: str):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = _prepare_key(key, alphabet)
    pairs = _prepare_text(text)

    out = []
    for i in range(0, len(pairs), 2):
        r1, c1 = _find(matrix, pairs[i])
        r2, c2 = _find(matrix, pairs[i+1])

        if r1 == r2:
            out.append(matrix[r1][(c1+1) % 5])
            out.append(matrix[r2][(c2+1) % 5])
        elif c1 == c2:
            out.append(matrix[(r1+1) % 5][c1])
            out.append(matrix[(r2+1) % 5][c2])
        else:
            out.append(matrix[r1][c2])
            out.append(matrix[r2][c1])

    return "".join(out)


def decrypt(text: str, key: str):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = _prepare_key(key, alphabet)

    out = []
    for i in range(0, len(text), 2):
        r1, c1 = _find(matrix, text[i])
        r2, c2 = _find(matrix, text[i+1])

        if r1 == r2:
            out.append(matrix[r1][(c1-1) % 5])
            out.append(matrix[r2][(c2-1) % 5])
        elif c1 == c2:
            out.append(matrix[(r1-1) % 5][c1])
            out.append(matrix[(r2-1) % 5][c2])
        else:
            out.append(matrix[r1][c2])
            out.append(matrix[r2][c1])

    return "".join(out)
