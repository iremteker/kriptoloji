def _clean_alphabet(alphabet: str) -> str:
    seen = set()
    out = []
    for ch in alphabet:
        if ch not in seen:
            seen.add(ch)
            out.append(ch)
    return "".join(out)


def _extend_key(text: str, key: str, alphabet: str) -> str:
    key = [k for k in key if k in alphabet or k.lower() in alphabet.lower()]
    if not key:
        raise ValueError("Anahtar, alfabetik karakterleri içermelidir.")

    extended = []
    idx = 0
    for ch in text:
        if ch in alphabet or ch.lower() in alphabet.lower():
            extended.append(key[idx % len(key)])
            idx += 1
        else:
            extended.append(ch)
    return "".join(extended)


def encrypt(plaintext: str, key: str, alphabet: str) -> str:
    alphabet = _clean_alphabet(alphabet)
    n = len(alphabet)
    key_ext = _extend_key(plaintext, key, alphabet)

    out = []
    for p, k in zip(plaintext, key_ext):
        if p in alphabet:
            pi = alphabet.index(p)
            ki = alphabet.index(k.upper())
            out.append(alphabet[(pi + ki) % n])
        elif p.lower() in alphabet.lower():
            pi = alphabet.lower().index(p.lower())
            ki = alphabet.lower().index(k.lower())
            out.append(alphabet.lower()[(pi + ki) % n])
        else:
            out.append(p)
    return "".join(out)


def decrypt(ciphertext: str, key: str, alphabet: str) -> str:
    alphabet = _clean_alphabet(alphabet)
    n = len(alphabet)
    key_ext = _extend_key(ciphertext, key, alphabet)

    out = []
    for c, k in zip(ciphertext, key_ext):
        if c in alphabet:
            ci = alphabet.index(c)
            ki = alphabet.index(k.upper())
            out.append(alphabet[(ci - ki) % n])
        elif c.lower() in alphabet.lower():
            ci = alphabet.lower().index(c.lower())
            ki = alphabet.lower().index(k.lower())
            out.append(alphabet.lower()[(ci - ki) % n])
        else:
            out.append(c)
    return "".join(out)
