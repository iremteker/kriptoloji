def encrypt(text: str, rails: int) -> str:
    if rails <= 1:
        return text

    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1

    for ch in text:
        fence[rail].append(ch)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    return "".join("".join(row) for row in fence)


def decrypt(cipher: str, rails: int) -> str:
    if rails <= 1:
        return cipher

    pattern = []
    rail = 0
    direction = 1
    for _ in cipher:
        pattern.append(rail)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    fence = [[] for _ in range(rails)]
    idx = 0
    for r in range(rails):
        for i, p in enumerate(pattern):
            if p == r:
                fence[r].append(cipher[idx])
                idx += 1

    out = []
    rail_pos = [0] * rails
    for p in pattern:
        out.append(fence[p][rail_pos[p]])
        rail_pos[p] += 1

    return "".join(out)
