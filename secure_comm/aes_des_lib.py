import os
from typing import Tuple

from cryptography.hazmat.primitives import padding as sympad
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from Crypto.Cipher import DES


def gen_aes_key() -> bytes:
    return os.urandom(16)  # AES-128


def gen_des_key() -> bytes:
    return os.urandom(8)   # DES-56 effective (8 bytes incl parity)


def aes_encrypt_cbc(key: bytes, plaintext: bytes) -> Tuple[bytes, bytes]:
    iv = os.urandom(16)
    padder = sympad.PKCS7(128).padder()
    padded = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    enc = cipher.encryptor()
    ct = enc.update(padded) + enc.finalize()
    return iv, ct


def aes_decrypt_cbc(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    dec = cipher.decryptor()
    padded = dec.update(ciphertext) + dec.finalize()

    unpadder = sympad.PKCS7(128).unpadder()
    pt = unpadder.update(padded) + unpadder.finalize()
    return pt


def des_encrypt_cbc(key: bytes, plaintext: bytes) -> Tuple[bytes, bytes]:
    iv = os.urandom(8)
    padder = sympad.PKCS7(64).padder()
    padded = padder.update(plaintext) + padder.finalize()

    cipher = DES.new(key, DES.MODE_CBC, iv=iv)
    ct = cipher.encrypt(padded)
    return iv, ct


def des_decrypt_cbc(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    cipher = DES.new(key, DES.MODE_CBC, iv=iv)
    padded = cipher.decrypt(ciphertext)

    unpadder = sympad.PKCS7(64).unpadder()
    pt = unpadder.update(padded) + unpadder.finalize()
    return pt
