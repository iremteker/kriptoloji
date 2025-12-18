import streamlit as st

from classical_ciphers.caesar import encrypt, decrypt

st.set_page_config(page_title="Kriptoloji Projesi", page_icon="🔐", layout="centered")

st.caption("Streamlit UI + Sezar Şifreleme (Encrypt / Decrypt)")


st.sidebar.header("Algoritma Seçimi")
algo = st.sidebar.selectbox("Şifreleme Yöntemi", ["Sezar (Caesar)"], index=0)

st.sidebar.divider()
st.sidebar.subheader("Alfabe")
alphabet_choice = st.sidebar.radio(
    "Hazır alfabe seç",
    ["İngilizce (A-Z)", "Türkçe (A-Z + ÇĞİÖŞÜ)", "Özel (Custom)"],
    index=1,
)

DEFAULT_EN = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DEFAULT_TR = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"

if alphabet_choice == "İngilizce (A-Z)":
    alphabet = DEFAULT_EN
elif alphabet_choice == "Türkçe (A-Z + ÇĞİÖŞÜ)":
    alphabet = DEFAULT_TR
else:
    alphabet = st.sidebar.text_input("Özel alfabet (benzersiz karakterlerden oluşsun)", value=DEFAULT_TR)

shift = st.sidebar.slider("Shift (Kaydırma) Değeri", min_value=0, max_value=max(1, len(alphabet) - 1), value=3)


if algo == "Sezar (Caesar)":
    st.subheader("Sezar Şifreleme")

    tab1, tab2 = st.tabs(["🔒 Encrypt", "🔓 Decrypt"])

    with tab1:
        plaintext = st.text_area("Plaintext (Açık metin)", height=140, placeholder="Mesajını buraya yaz...")
        colA, colB = st.columns(2)
        with colA:
            run_enc = st.button("Encrypt", type="primary", use_container_width=True)
        with colB:
            clear_enc = st.button("Temizle (Encrypt)", use_container_width=True)

        if clear_enc:
            st.session_state["enc_out"] = ""
            st.rerun()

        if run_enc:
            try:
                res = encrypt(plaintext, shift=shift, alphabet=alphabet)
                st.session_state["enc_out"] = res.text
            except Exception as e:
                st.error(f"Hata: {e}")

        enc_out = st.session_state.get("enc_out", "")
        st.text_area("Ciphertext (Şifreli metin)", value=enc_out, height=140)

        st.caption(f"Kullanılan alfabet: `{alphabet}` | Shift: `{shift}`")

    with tab2:
        ciphertext = st.text_area("Ciphertext (Şifreli metin)", height=140, placeholder="Şifreli mesajı buraya yapıştır...")
        colC, colD = st.columns(2)
        with colC:
            run_dec = st.button("Decrypt", type="primary", use_container_width=True)
        with colD:
            clear_dec = st.button("Temizle (Decrypt)", use_container_width=True)

        if clear_dec:
            st.session_state["dec_out"] = ""
            st.rerun()

        if run_dec:
            try:
                res = decrypt(ciphertext, shift=shift, alphabet=alphabet)
                st.session_state["dec_out"] = res.text
            except Exception as e:
                st.error(f"Hata: {e}")

        dec_out = st.session_state.get("dec_out", "")
        st.text_area("Plaintext (Açık metin)", value=dec_out, height=140)

        st.caption(f"Kullanılan alfabet: `{alphabet}` | Shift: `{shift}`")

