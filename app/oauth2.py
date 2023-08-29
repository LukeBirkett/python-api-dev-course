from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme  = OAuth2PasswordBearer(tokenUrl='login')

# SECRET KEY
# Algorithm HS256
# Expiration time of token

SECRET_KEY = "ee4aa7d036c8ba50f15926b9e32923f4419991884254cd1f7054e5f74c357ad5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

def verify_access_token(token: str, credentials_exeption):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exeption
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exeption
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="could not validiate",
        headers={"WWW-Authenticate": "Bearer"} 
        )
    return verify_access_token(token, credentials_exeption)
