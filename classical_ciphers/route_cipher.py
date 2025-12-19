def encrypt(text: str, cols: int) -> str:
    rows = (len(text) + cols - 1) // cols
    grid = [[""] * cols for _ in range(rows)]

    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx < len(text):
                grid[r][c] = text[idx]
                idx += 1

    out = []
    for c in range(cols):
        for r in range(rows):
            out.append(grid[r][c])
    return "".join(out)


def decrypt(cipher: str, cols: int) -> str:
    rows = (len(cipher) + cols - 1) // cols
    grid = [[""] * cols for _ in range(rows)]

    idx = 0
    for c in range(cols):
        for r in range(rows):
            if idx < len(cipher):
                grid[r][c] = cipher[idx]
                idx += 1

    return "".join("".join(r) for r in grid).rstrip()
