from manual_cipher.simplified_aes import encrypt, decrypt

key = "ABCD"
plaintext = "FACE"   # sadece A–P arası

cipher_state = encrypt(plaintext, key)
print("Cipher state:", cipher_state)

decrypted = decrypt(cipher_state, key)
print("Decrypted:", decrypted)