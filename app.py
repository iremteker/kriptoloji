import streamlit as st

from classical_ciphers.caesar import encrypt as caesar_encrypt, decrypt as caesar_decrypt
from classical_ciphers.substitution import encrypt as sub_encrypt, decrypt as sub_decrypt
from classical_ciphers.vigenere import encrypt as vig_encrypt, decrypt as vig_decrypt

st.set_page_config(page_title="Kriptoloji", page_icon="🔐")

DEFAULT_EN = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DEFAULT_TR = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"

st.sidebar.selectbox(
    "Algoritma",
    ["Sezar", "Substitution", "Vigenère"],
    key="algo"
)

alphabet = st.sidebar.selectbox(
    "Alfabe",
    ["Türkçe", "İngilizce"],
)
alphabet = DEFAULT_TR if alphabet == "Türkçe" else DEFAULT_EN

st.title(st.session_state.algo)

if st.session_state.algo == "Sezar":
    shift = st.slider("Shift", 0, len(alphabet) - 1, 3)

    p = st.text_area("Plaintext")
    if st.button("Encrypt"):
        st.text_area("Ciphertext", caesar_encrypt(p, shift, alphabet).text)

    c = st.text_area("Ciphertext ")
    if st.button("Decrypt"):
        st.text_area("Plaintext ", caesar_decrypt(c, shift, alphabet).text)


elif st.session_state.algo == "Substitution":
    key_alpha = st.text_input("Key Alphabet", value=alphabet)

    p = st.text_area("Plaintext")
    if st.button("Encrypt"):
        st.text_area("Ciphertext", sub_encrypt(p, key_alpha, alphabet))

    c = st.text_area("Ciphertext ")
    if st.button("Decrypt"):
        st.text_area("Plaintext ", sub_decrypt(c, key_alpha, alphabet))


elif st.session_state.algo == "Vigenère":
    key = st.text_input("Key")

    p = st.text_area("Plaintext")
    if st.button("Encrypt"):
        st.text_area("Ciphertext", vig_encrypt(p, key, alphabet))

    c = st.text_area("Ciphertext ")
    if st.button("Decrypt"):
        st.text_area("Plaintext ", vig_decrypt(c, key, alphabet))
