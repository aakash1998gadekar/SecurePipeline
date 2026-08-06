from backend.app.services.crypto import encrypt_value, decrypt_value


def test_encrypt_decrypt_roundtrip():
    original = "my-secret-api-key-12345"
    encrypted = encrypt_value(original)
    assert encrypted != original
    assert decrypt_value(encrypted) == original


def test_different_inputs_produce_different_ciphertext():
    enc1 = encrypt_value("secret1")
    enc2 = encrypt_value("secret2")
    assert enc1 != enc2
