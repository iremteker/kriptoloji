import socket
import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

SERVER_HOST = '127.0.0.1'  # sunucu IP'si
SERVER_PORT = 65432

class App:
    def __init__(self, master):
        self.master = master
        master.title("Şifreli Gönderici - Client")

        tk.Label(master, text="Sunucu IP:").grid(row=0, column=0, sticky='e')
        self.ip_entry = tk.Entry(master)
        self.ip_entry.insert(0, SERVER_HOST)
        self.ip_entry.grid(row=0, column=1)

        tk.Label(master, text="Sunucu Port:").grid(row=1, column=0, sticky='e')
        self.port_entry = tk.Entry(master)
        self.port_entry.insert(0, str(SERVER_PORT))
        self.port_entry.grid(row=1, column=1)

        tk.Label(master, text="Gönderilecek Metin:").grid(row=2, column=0, sticky='ne')
        self.text_box = tk.Text(master, height=8, width=40)
        self.text_box.grid(row=2, column=1)

        self.send_btn = tk.Button(master, text="Bağlan ve Gönder", command=self.connect_and_send)
        self.send_btn.grid(row=3, column=1, pady=10)

    def connect_and_send(self):
        server_ip = self.ip_entry.get().strip()
        server_port = int(self.port_entry.get().strip())
        msg = self.text_box.get("1.0", tk.END).strip()
        if not msg:
            messagebox.showwarning("Uyarı", "Gönderecek bir metin gir.")
            return

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((server_ip, server_port))
                # 1) Sunucudan public key'i al
                raw_len = s.recv(4)
                pub_len = int.from_bytes(raw_len, 'big')
                pub_bytes = b''
                while len(pub_bytes) < pub_len:
                    pub_bytes += s.recv(pub_len - len(pub_bytes))
                # yükle
                server_pub = serialization.load_pem_public_key(pub_bytes)

                # 2) AES anahtarı üret ve RSA ile şifreleyip gönder
                aes_key = AESGCM.generate_key(bit_length=256)
                enc_key = server_pub.encrypt(
                    aes_key,
                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                 algorithm=hashes.SHA256(),
                                 label=None)
                )
                s.sendall(len(enc_key).to_bytes(4, 'big') + enc_key)

                # 3) Mesajı AES-GCM ile şifrele ve gönder (nonce + length + ciphertext)
                aesgcm = AESGCM(aes_key)
                nonce = os.urandom(12)  # GCM nonce 12 byte önerilir
                ciphertext = aesgcm.encrypt(nonce, msg.encode('utf-8'), None)

                s.sendall(len(nonce).to_bytes(4, 'big') + nonce)
                s.sendall(len(ciphertext).to_bytes(4, 'big') + ciphertext)

                messagebox.showinfo("Başarılı", "Mesaj gönderildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Bağlantı/gönderim hatası:\n{e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
