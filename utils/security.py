# utils/security.py
import hashlib

# 加密密码
def get_hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# 验证密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_hash_password(plain_password) == hashed_password