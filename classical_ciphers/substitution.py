def _clean_alphabet(alphabet: str) -> str:
    seen = set()
    out = []
    for ch in alphabet:
        if ch not in seen:
            seen.add(ch)
            out.append(ch)
    return "".join(out)


def encrypt(plaintext: str, key_alphabet: str, base_alphabet: str) -> str:
    base = _clean_alphabet(base_alphabet)
    key = _clean_alphabet(key_alphabet)

    if len(base) != len(key):
        raise ValueError("Temel alfabe ve anahtar alfabe aynı uzunlukta olmalıdır.")

    enc_map = {base[i]: key[i] for i in range(len(base))}
    enc_map_lower = {base[i].lower(): key[i].lower() for i in range(len(base))}

    out = []
    for ch in plaintext:
        if ch in enc_map:
            out.append(enc_map[ch])
        elif ch in enc_map_lower:
            out.append(enc_map_lower[ch])
        else:
            out.append(ch)
    return "".join(out)


def decrypt(ciphertext: str, key_alphabet: str, base_alphabet: str) -> str:
    base = _clean_alphabet(base_alphabet)
    key = _clean_alphabet(key_alphabet)

    if len(base) != len(key):
        raise ValueError("Temel alfabe ve anahtar alfabe aynı uzunlukta olmalıdır.")

    dec_map = {key[i]: base[i] for i in range(len(base))}
    dec_map_lower = {key[i].lower(): base[i].lower() for i in range(len(base))}

    out = []
    for ch in ciphertext:
        if ch in dec_map:
            out.append(dec_map[ch])
        elif ch in dec_map_lower:
            out.append(dec_map_lower[ch])
        else:
            out.append(ch)
    return "".join(out)
