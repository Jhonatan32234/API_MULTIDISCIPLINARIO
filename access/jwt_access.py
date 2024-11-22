import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends,Header
from dotenv import load_dotenv
import os

# Cargar las variables de entorno
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")  # Cambia por tu clave secreta
ALGORITHM = "HS256"  # Algoritmo de encriptación
ACCESS_TOKEN_EXPIRE_MINUTES = 300  # Tiempo de expiración del token en minutos

# Crear un token de acceso
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_jwt_token(authorization: str = Header(...)):
    try:
        # Elimina el prefijo "Bearer" si está presente
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Formato de token inválido")
        
        token = authorization.split(" ")[1]  # Extrae el token real
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if not exp or exp < datetime.utcnow().timestamp():
            raise HTTPException(status_code=401, detail="El token ha expirado.")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido.")

    
def get_token(payload: dict = Depends(validate_jwt_token)):
    return payload 



def verify_role(required_roles: list[str]):
    def role_checker(payload: dict = Depends(get_token)):
        token_role = payload.get("rol")
        if token_role not in required_roles:
            raise HTTPException(
                status_code=403,
                detail=f"No tienes permiso para esta acción. Se requiere uno de los siguientes roles: {', '.join(required_roles)}"
            )
        return payload
    return Depends(role_checker)
