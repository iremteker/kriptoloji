import argparse
import base64
import socket

from secure_comm.protocol import send_frame, recv_frame
from secure_comm.rsa_key_exchange import load_public_key_from_pem, rsa_encrypt
from secure_comm.aes_des_lib import (
    gen_aes_key, gen_des_key,
    aes_encrypt_cbc, des_encrypt_cbc,
    aes_decrypt_cbc, des_decrypt_cbc
)


def b64e(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")


def b64d(s: str) -> bytes:
    return base64.b64decode(s.encode("ascii"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=5000)
    ap.add_argument("--algo", choices=["AES", "DES"], required=True)
    ap.add_argument("--msg", required=True)
    args = ap.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((args.host, args.port))

        # 1) server public key alma
        hello = recv_frame(sock)
        if hello.get("type") != "server_pubkey":
            raise ValueError("Expected server_pubkey")
        pub_pem = b64d(hello["pem"])
        pub = load_public_key_from_pem(pub_pem)

        # 2) simetrik anahtar oluşturma + şifrelenmiş anahtarı gönderme
        if args.algo == "AES":
            sym_key = gen_aes_key()
        else:
            sym_key = gen_des_key()

        enc_key = rsa_encrypt(pub, sym_key)
        send_frame(sock, {"type": "key", "algo": args.algo, "enc_key": b64e(enc_key)})

        # 3) şifrelenmiş mesaj gönderme
        pt = args.msg.encode("utf-8")
        if args.algo == "AES":
            iv, ct = aes_encrypt_cbc(sym_key, pt)
        else:
            iv, ct = des_encrypt_cbc(sym_key, pt)

        send_frame(sock, {"type": "data", "iv": b64e(iv), "ct": b64e(ct)})

        # 4) ACK alma
        ack = recv_frame(sock)
        if ack.get("type") == "ack":
            aiv = b64d(ack["iv"])
            act = b64d(ack["ct"])
            if args.algo == "AES":
                apt = aes_decrypt_cbc(sym_key, aiv, act)
            else:
                apt = des_decrypt_cbc(sym_key, aiv, act)
            print("[CLIENT] ack plaintext:", apt.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
