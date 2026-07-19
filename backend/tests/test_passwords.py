from app.auth.passwords import PasswordHasher


def test_hash_verify_returns_true():
    hasher = PasswordHasher()
    assert hasher.verify("password", hasher.hash("password"))


def test_hash_verify_returns_false():
    hasher = PasswordHasher()
    assert not hasher.verify("password", hasher.hash("password_test"))
