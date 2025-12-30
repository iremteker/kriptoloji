PIGPEN_MAP = {
    "A": "┌", "B": "┬", "C": "┐",
    "D": "├", "E": "┼", "F": "┤",
    "G": "└", "H": "┴", "I": "┘",

    "J": "┌•", "K": "┬•", "L": "┐•",
    "M": "├•", "N": "┼•", "O": "┤•",
    "P": "└•", "Q": "┴•", "R": "┘•",

    "S": "╲╱", "T": "╱╲",
    "U": "╳",  "V": "╱╱",

    "W": "╲╱•", "X": "╱╲•",
    "Y": "╳•",  "Z": "╱╱•",
}


REVERSE_MAP = {v: k for k, v in PIGPEN_MAP.items()}


def encrypt(text: str) -> str:
    out = []
    for ch in text.upper():
        if ch in PIGPEN_MAP:
            out.append(PIGPEN_MAP[ch])
        else:
            out.append(ch)
    return " ".join(out)


def decrypt(text: str) -> str:
    out = []
    tokens = text.split()

    for token in tokens:
        out.append(REVERSE_MAP.get(token, token))

    return "".join(out)
