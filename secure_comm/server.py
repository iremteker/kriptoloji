import base64
import socket

from secure_comm.protocol import send_frame, recv_frame
from secure_comm.rsa_key_exchange import generate_rsa_keypair, public_key_to_pem, rsa_decrypt
from secure_comm.aes_des_lib import aes_decrypt_cbc, des_decrypt_cbc, aes_encrypt_cbc, des_encrypt_cbc


HOST = "0.0.0.0"
PORT = 5000


def b64e(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")


def b64d(s: str) -> bytes:
    return base64.b64decode(s.encode("ascii"))


def main():
    priv, pub = generate_rsa_keypair()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[SERVER] listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        with conn:
            print(f"[SERVER] connected: {addr}")

            # 1) public key gönderme
            send_frame(conn, {"type": "server_pubkey", "pem": b64e(public_key_to_pem(pub))})

            # 2) şifrelenmiş simetrik key alma
            msg = recv_frame(conn)
            if msg.get("type") != "key":
                raise ValueError("Expected key frame")

            algo = msg["algo"]  # "AES" veya "DES"
            enc_key = b64d(msg["enc_key"])
            sym_key = rsa_decrypt(priv, enc_key)

            # 3) encrypted data alma
            data = recv_frame(conn)
            if data.get("type") != "data":
                raise ValueError("Expected data frame")

            iv = b64d(data["iv"])
            ct = b64d(data["ct"])

            if algo == "AES":
                pt = aes_decrypt_cbc(sym_key, iv, ct)
            elif algo == "DES":
                pt = des_decrypt_cbc(sym_key, iv, ct)
            else:
                raise ValueError("Unsupported algo")

            print("[SERVER] plaintext:", pt.decode("utf-8", errors="replace"))

            # isteğe bağlı ACK
            ack_text = b"ACK"
            if algo == "AES":
                ack_iv, ack_ct = aes_encrypt_cbc(sym_key, ack_text)
            else:
                ack_iv, ack_ct = des_encrypt_cbc(sym_key, ack_text)

            send_frame(conn, {"type": "ack", "iv": b64e(ack_iv), "ct": b64e(ack_ct)})


if __name__ == "__main__":
    main()
