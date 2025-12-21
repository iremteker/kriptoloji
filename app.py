import streamlit as st

from classical_ciphers.caesar import encrypt as caesar_encrypt, decrypt as caesar_decrypt
from classical_ciphers.substitution import encrypt as sub_encrypt, decrypt as sub_decrypt
from classical_ciphers.vigenere import encrypt as vig_encrypt, decrypt as vig_decrypt
from classical_ciphers.rail_fence import encrypt as rf_encrypt, decrypt as rf_decrypt
from classical_ciphers.columnar import encrypt as col_encrypt, decrypt as col_decrypt
from classical_ciphers.route_cipher import encrypt as rt_encrypt, decrypt as rt_decrypt
from classical_ciphers.playfair import encrypt as pf_encrypt, decrypt as pf_decrypt
from classical_ciphers.polybius import encrypt as pb_encrypt, decrypt as pb_decrypt
from classical_ciphers.pigpen import encrypt as pg_encrypt, decrypt as pg_decrypt
from classical_ciphers.hill import encrypt as hill_encrypt, decrypt as hill_decrypt
from secure_comm.aes_des_lib import (gen_aes_key, gen_des_key, aes_encrypt_cbc, aes_decrypt_cbc, des_encrypt_cbc, des_decrypt_cbc)
import base64


st.set_page_config(page_title="Kriptoloji", page_icon="🔐")

DEFAULT_EN = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DEFAULT_TR = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"

algo = st.sidebar.selectbox(
    "Algoritma",
    ["Sezar", "Substitution", "Vigenère", 
    "Rail Fence", "Columnar", "Route", 
    "Playfair", "Polybius", "Pigpen", 
    "Hill", "AES (Library)", "AES (Manual – Simplified)", "DES (Library)"]
    )

alphabet = st.sidebar.selectbox("Alfabe", ["Türkçe", "İngilizce"])
alphabet = DEFAULT_TR if alphabet == "Türkçe" else DEFAULT_EN

st.title(algo)

if algo == "Sezar":
    shift = st.slider("Shift", 0, len(alphabet) - 1, 3)
    p = st.text_area("Plaintext")
    if st.button("Encrypt"):
        st.text_area("Ciphertext", caesar_encrypt(p, shift, alphabet).text)
    c = st.text_area("Ciphertext ")
    if st.button("Decrypt"):
        st.text_area("Plaintext ", caesar_decrypt(c, shift, alphabet).text)

elif algo == "Substitution":
    key_alpha = st.text_input("Key Alphabet", value=alphabet)
    p = st.text_area("Plaintext")
    if st.button("Encrypt"):
        st.text_area("Ciphertext", sub_encrypt(p, key_alpha, alphabet))
    c = st.text_area("Ciphertext ")
    if st.button("Decrypt"):
        st.text_area("Plaintext ", sub_decrypt(c, key_alpha, alphabet))

elif algo == "Vigenère":
    key = st.text_input("Key")
    p = st.text_area("Plaintext")
    if st.button("Encrypt"):
        st.text_area("Ciphertext", vig_encrypt(p, key, alphabet))
    c = st.text_area("Ciphertext ")
    if st.button("Decrypt"):
        st.text_area("Plaintext ", vig_decrypt(c, key, alphabet))

elif algo == "Rail Fence":
    rails = st.slider("Rails", 2, 10, 3)
    p = st.text_area("Plaintext")
    if st.button("Encrypt"):
        st.text_area("Ciphertext", rf_encrypt(p, rails))
    c = st.text_area("Ciphertext ")
    if st.button("Decrypt"):
        st.text_area("Plaintext ", rf_decrypt(c, rails))

elif algo == "Columnar":
    key = st.text_input("Key")
    p = st.text_area("Plaintext")
    if st.button("Encrypt"):
        st.text_area("Ciphertext", col_encrypt(p, key))
    c = st.text_area("Ciphertext ")
    if st.button("Decrypt"):
        st.text_area("Plaintext ", col_decrypt(c, key))

elif algo == "Route":
    cols = st.slider("Columns", 2, 10, 4)
    p = st.text_area("Plaintext")
    if st.button("Encrypt"):
        st.text_area("Ciphertext", rt_encrypt(p, cols))
    c = st.text_area("Ciphertext ")
    if st.button("Decrypt"):
        st.text_area("Plaintext ", rt_decrypt(c, cols))

elif algo == "Playfair":
    key = st.text_input("Key")
    p = st.text_area("Plaintext")
    if st.button("Encrypt"):
        st.text_area("Ciphertext", pf_encrypt(p, key))
    c = st.text_area("Ciphertext ")
    if st.button("Decrypt"):
        st.text_area("Plaintext ", pf_decrypt(c, key))

elif algo == "Polybius":
    p = st.text_area("Plaintext")
    if st.button("Encrypt"):
        st.text_area("Ciphertext", pb_encrypt(p))
    c = st.text_area("Ciphertext ")
    if st.button("Decrypt"):
        st.text_area("Plaintext ", pb_decrypt(c))

elif algo == "Pigpen":
    p = st.text_area("Plaintext")
    if st.button("Encrypt"):
        st.text_area("Ciphertext", pg_encrypt(p))
    c = st.text_area("Ciphertext ")
    if st.button("Decrypt"):
        st.text_area("Plaintext ", pg_decrypt(c))


if algo == "Hill":
    st.subheader("2x2 Key Matrix")

    c1, c2 = st.columns(2)
    with c1:
        a = st.number_input("a", value=3)
        b = st.number_input("b", value=3)
    with c2:
        c = st.number_input("c", value=2)
        d = st.number_input("d", value=5)

    key = [[a, b], [c, d]]

    p = st.text_area("Plaintext")
    if st.button("Encrypt"):
        try:
            st.text_area("Ciphertext", hill_encrypt(p, key))
        except Exception as e:
            st.error(e)

    ciph = st.text_area("Ciphertext ")
    if st.button("Decrypt"):
        try:
            st.text_area("Plaintext ", hill_decrypt(ciph, key))
        except Exception as e:
            st.error(e)


elif algo == "AES (Library)":
    key = gen_aes_key()
    st.text("AES-128 (CBC Mode)")

    plaintext = st.text_area("Plaintext")
    if st.button("Encrypt"):
        iv, ct = aes_encrypt_cbc(key, plaintext.encode())
        st.session_state["aes"] = (key, iv, ct)
        st.text_area("Ciphertext (Base64)", base64.b64encode(ct).decode())

    if "aes" in st.session_state and st.button("Decrypt"):
        key, iv, ct = st.session_state["aes"]
        pt = aes_decrypt_cbc(key, iv, ct)
        st.text_area("Decrypted Plaintext", pt.decode())

    elif algo == "AES (Manual – Simplified)":
        st.text("Sadeleştirilmiş AES (kütüphanesiz)")
        st.text("Bu implementasyon terminal üzerinden test edilmiştir.")
        st.text("Dosya: manual_cipher/simplified_aes.py")
        st.text("Test: python test_manual_aes.py")


elif algo == "DES (Library)":
    key = gen_des_key()
    st.text("DES (CBC Mode)")

    plaintext = st.text_area("Plaintext")
    if st.button("Encrypt"):
        iv, ct = des_encrypt_cbc(key, plaintext.encode())
        st.session_state["des"] = (key, iv, ct)
        st.text_area("Ciphertext (Base64)", base64.b64encode(ct).decode())

    if "des" in st.session_state and st.button("Decrypt"):
        key, iv, ct = st.session_state["des"]
        pt = des_decrypt_cbc(key, iv, ct)
        st.text_area("Decrypted Plaintext", pt.decode())
