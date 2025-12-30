from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CaesarResult:
    text: str
    used_alphabet: str
    shift: int


def _build_maps(alphabet: str, shift: int):
    seen = set()
    cleaned = []
    for ch in alphabet:
        if ch not in seen:
            cleaned.append(ch)
            seen.add(ch)

    if len(cleaned) < 2:
        raise ValueError("Alfabe en az 2 farklı karakter içermelidir.")

    alph = "".join(cleaned)
    n = len(alph)
    s = shift % n

    enc_map = {alph[i]: alph[(i + s) % n] for i in range(n)}
    dec_map = {alph[(i + s) % n]: alph[i] for i in range(n)}
    return alph, enc_map, dec_map


def encrypt(plaintext: str, shift: int, alphabet: str) -> CaesarResult:
    """
    Özel bir alfabe üzerinden Sezar şifrelemesi.
    Alfabede bulunmayan karakterler değiştirilmez.
    Aynı alfabe kümesindeki küçük harfle eşleşen harfler için büyük/küçük harf koruması.
    """
    alph, enc_map, _ = _build_maps(alphabet, shift)


    lower_alph = "".join(ch.lower() for ch in alph)
    _, enc_map_lower, _ = _build_maps(lower_alph, shift)

    out = []
    for ch in plaintext:
        if ch in enc_map:
            out.append(enc_map[ch])
        elif ch in enc_map_lower:
            out.append(enc_map_lower[ch])
        else:
            out.append(ch)

    return CaesarResult(text="".join(out), used_alphabet=alph, shift=shift % len(alph))


def decrypt(ciphertext: str, shift: int, alphabet: str) -> CaesarResult:
    """
    Sezar şifresinin özel bir alfabe üzerinden çözülmesi.
    """
    alph, _, dec_map = _build_maps(alphabet, shift)

    lower_alph = "".join(ch.lower() for ch in alph)
    _, _, dec_map_lower = _build_maps(lower_alph, shift)

    out = []
    for ch in ciphertext:
        if ch in dec_map:
            out.append(dec_map[ch])
        elif ch in dec_map_lower:
            out.append(dec_map_lower[ch])
        else:
            out.append(ch)

    return CaesarResult(text="".join(out), used_alphabet=alph, shift=shift % len(alph))
