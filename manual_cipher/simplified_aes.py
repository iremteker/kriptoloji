S_BOX = {
    0x0: 0x9, 0x1: 0x4, 0x2: 0xA, 0x3: 0xB,
    0x4: 0xD, 0x5: 0x1, 0x6: 0x8, 0x7: 0x5,
    0x8: 0x6, 0x9: 0x2, 0xA: 0x0, 0xB: 0x3,
    0xC: 0xC, 0xD: 0xE, 0xE: 0xF, 0xF: 0x7,
}
INV_S_BOX = {v: k for k, v in S_BOX.items()}

ALPHABET = "ABCDEFGHIJKLMNOP"  # 16 karakter = 4 bit


def text_to_state(text):
    return [ALPHABET.index(c) for c in text]


def state_to_text(state):
    return "".join(ALPHABET[x] for x in state)


def sub_bytes(state):
    return [S_BOX[x] for x in state]


def inv_sub_bytes(state):
    return [INV_S_BOX[x] for x in state]


def shift_rows(state):
    return [state[0], state[1], state[3], state[2]]


def inv_shift_rows(state):
    return [state[0], state[1], state[3], state[2]]


def add_round_key(state, key):
    return [state[i] ^ key[i] for i in range(len(state))]


def encrypt(plaintext: str, key: str):
    state = text_to_state(plaintext)
    round_key = text_to_state(key)

    # Round 1
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_key)

    # Round 2
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_key)

    return state


def decrypt(cipher_state, key: str):
    state = cipher_state
    round_key = text_to_state(key)

    # Round 2
    state = add_round_key(state, round_key)
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)

    # Round 1
    state = add_round_key(state, round_key)
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)

    return state_to_text(state)
