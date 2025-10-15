import socket
import threading
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HOST = '0.0.0.0'   # tüm interfaceler
PORT = 65432

# RSA anahtar çifti oluştur
def generate_rsa_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def public_key_bytes(pubkey):
    return pubkey.public_bytes(encoding=serialization.Encoding.PEM,
                               format=serialization.PublicFormat.SubjectPublicKeyInfo)

def handle_client(conn, addr, private_key):
    try:
        print(f"[+] Bağlandı: {addr}")

        # 1) Sunucu -> istemci : public key gönder
        pub_bytes = public_key_bytes(private_key.public_key())
        conn.sendall(len(pub_bytes).to_bytes(4, 'big') + pub_bytes)

        # 2) İstemciden RSA ile şifrelenmiş AES anahtarını al
        # ilk 4 byte uzunluk bilgisi
        data = conn.recv(4)
        if not data:
            print("Beklenmedik bağlantı kapandı (anahtar).")
            return
        enc_key_len = int.from_bytes(data, 'big')
        enc_key = b''
        while len(enc_key) < enc_key_len:
            chunk = conn.recv(enc_key_len - len(enc_key))
            if not chunk:
                break
            enc_key += chunk

        # RSA ile AES anahtarını çöz
        aes_key = private_key.decrypt(
            enc_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None)
        )
        print("[*] AES anahtarı alındı ve çözüldü.")

        # 3) Gelen şifreli mesajları al ve çöz
        # Protokol: önce 4 byte nonce uzunluğu, nonce, 4 byte ciphertext uzunluğu, ciphertext
        while True:
            hdr = conn.recv(4)
            if not hdr:
                print("Bağlantı kapandı.")
                break
            nonce_len = int.from_bytes(hdr, 'big')
            nonce = conn.recv(nonce_len)
            ct_len_bytes = conn.recv(4)
            if not ct_len_bytes:
                break
            ct_len = int.from_bytes(ct_len_bytes, 'big')
            ciphertext = b''
            while len(ciphertext) < ct_len:
                chunk = conn.recv(ct_len - len(ciphertext))
                if not chunk:
                    break
                ciphertext += chunk

            # AES-GCM ile deşifre et
            aesgcm = AESGCM(aes_key)
            try:
                plaintext = aesgcm.decrypt(nonce, ciphertext, None)
                print(f"[DECRYPTED from {addr}] {plaintext.decode('utf-8')}")
            except Exception as e:
                print("🔒 Decryption error:", e)
    except Exception as e:
        print("Hata (client handler):", e)
    finally:
        conn.close()

def main():
    private_key, public_key = generate_rsa_keypair()
    print("[*] RSA anahtar çifti oluşturuldu.")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[+] Sunucu dinlemede: {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr, private_key), daemon=True)
            t.start()

if __name__ == '__main__':
    main()
