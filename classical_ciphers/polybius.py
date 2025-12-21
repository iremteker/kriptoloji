def encrypt(text: str):
    square = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    out = []

    for ch in text.upper():
        if ch == "J":
            ch = "I"
        if ch in square:
            idx = square.index(ch)
            row = idx // 5 + 1
            col = idx % 5 + 1
            out.append(f"{row}{col}")
        else:
            out.append(ch)

    return " ".join(out)


def decrypt(text: str):
    square = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    out = []
    parts = text.split()

    for p in parts:
        if p.isdigit() and len(p) == 2:
            row = int(p[0]) - 1
            col = int(p[1]) - 1
            out.append(square[row * 5 + col])
        else:
            out.append(p)

    return "".join(out)
