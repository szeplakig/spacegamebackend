import bcrypt


def salt_and_hash_password(password: str, salt_str: str | None = None, rounds: int = 12) -> tuple[str, str]:
    password_bytes = password.encode("UTF-8")
    salt = salt_str.encode("UTF-8") if salt_str else bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(password_bytes, salt)
    hashed = hashed[len(salt) :]
    return salt.decode("UTF-8"), hashed.decode("UTF-8")
