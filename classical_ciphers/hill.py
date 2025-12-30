import math

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _modinv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Matris determinantının modüler tersi yoktur.")


def _matrix_det_2x2(m):
    return (m[0][0] * m[1][1] - m[0][1] * m[1][0]) % 26


def _matrix_inv_2x2(m):
    det = _matrix_det_2x2(m)
    inv_det = _modinv(det, 26)

    return [
        [( m[1][1] * inv_det) % 26, (-m[0][1] * inv_det) % 26],
        [(-m[1][0] * inv_det) % 26, ( m[0][0] * inv_det) % 26],
    ]


def _clean_text(text):
    return "".join([c for c in text.upper() if c in ALPHABET])


def encrypt(text: str, key_matrix):
    text = _clean_text(text)
    if len(text) % 2 != 0:
        text += "X"

    out = []
    for i in range(0, len(text), 2):
        v = [
            ALPHABET.index(text[i]),
            ALPHABET.index(text[i + 1])
        ]
        c0 = (key_matrix[0][0] * v[0] + key_matrix[0][1] * v[1]) % 26
        c1 = (key_matrix[1][0] * v[0] + key_matrix[1][1] * v[1]) % 26
        out.append(ALPHABET[c0])
        out.append(ALPHABET[c1])

    return "".join(out)


def decrypt(cipher: str, key_matrix):
    inv = _matrix_inv_2x2(key_matrix)
    out = []

    for i in range(0, len(cipher), 2):
        v = [
            ALPHABET.index(cipher[i]),
            ALPHABET.index(cipher[i + 1])
        ]
        p0 = (inv[0][0] * v[0] + inv[0][1] * v[1]) % 26
        p1 = (inv[1][0] * v[0] + inv[1][1] * v[1]) % 26
        out.append(ALPHABET[p0])
        out.append(ALPHABET[p1])

    return "".join(out)
