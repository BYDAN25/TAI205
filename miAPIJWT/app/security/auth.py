from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

#  Configuración
SECRET_KEY = "mi_secreto_super_seguro"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#  OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#  Encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#  Usuario fake (hash se genera UNA vez)
fake_user = {
    "username": "daniel",
    "password": pwd_context.hash("1234")
}

#  Verificar password
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

#  Autenticar usuario
def authenticate_user(username: str, password: str):
    if username != fake_user["username"]:
        return False
    if not verify_password(password, fake_user["password"]):
        return False
    return {"username": username}

#  Crear token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
        "sub": data.get("sub")  # 🔥 asegurar que siempre tenga subject
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#  Validar token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},  # 🔥 importante para Swagger
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        return {"username": username}

    except JWTError:
        raise credentials_exception