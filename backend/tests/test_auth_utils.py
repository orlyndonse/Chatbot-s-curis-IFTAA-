from src.auth.utils import generate_passwd_hash, verify_password

def test_password_verification_logic():
    """
    Teste la logique de hachage et de vérification de mot de passe de manière isolée.
    """
    password = "my_secure_password_123"
    hashed_password = generate_passwd_hash(password)

    # Scénario 1: Vérifie qu'un mot de passe correct est validé
    assert verify_password(password, hashed_password) is True

    # Scénario 2: Vérifie qu'un mot de passe incorrect est rejeté
    assert verify_password("wrong_password", hashed_password) is False

    # Scénario 3: Vérifie qu'un autre mot de passe incorrect est aussi rejeté
    assert verify_password("my_secure_password_123 ", hashed_password) is False