from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hash_password(password: str) -> str:
    return pwd_context.hash(password)
