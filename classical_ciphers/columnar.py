def _order_key(key: str):
    return sorted(list(enumerate(key)), key=lambda x: (x[1], x[0]))


def encrypt(text: str, key: str) -> str:
    n = len(key)
    rows = [text[i:i+n] for i in range(0, len(text), n)]
    rows[-1] = rows[-1].ljust(n)

    order = _order_key(key)
    out = []
    for idx, _ in order:
        for r in rows:
            out.append(r[idx])
    return "".join(out)


def decrypt(cipher: str, key: str) -> str:
    n = len(key)
    rows = len(cipher) // n
    order = _order_key(key)

    table = [[""] * n for _ in range(rows)]
    idx = 0
    for col, _ in order:
        for r in range(rows):
            table[r][col] = cipher[idx]
            idx += 1

    return "".join("".join(r) for r in table).rstrip()
