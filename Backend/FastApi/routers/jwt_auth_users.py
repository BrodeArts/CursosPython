from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter()

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1

#En vez de inventarme el secret, lo he generado así en la terminal >>openssl rand -hex 32
SECRET = "eb08a0e6d2211023494a6e5267d38f022a44b6edfd869f5dfc0a6689cf2fd022"

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str



users_db = {
    "brodearts": {
        "username": "brodearts",
        "full_name": "Antonio Díaz",
        "email": "antonio@diazfernandez.es",
        "disabled": False,
        "password": "$2a$12$h4EPglXCd.KDhbU3LIOBSOEPcyPNBpgfFzqlNk.OBJ.NZMMToZxeu"
    },
    "brodearts2": {
        "username": "brodearts2",
        "full_name": "Antonio Díaz2",
        "email": "antonio@diazfernandez.es2",
        "disabled": True,
        "password": "$2a$12$lGzIoyUj6BIwkJmH7grsw.JpU87G3Zg5oP99Gszmtf4TGSZTkwhOm"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticacion inválidas", 
            headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception


    except JWTError:
        raise exception
        
    return search_user(username)
    
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo")
    
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {"sub": user.username, "exp": expire, }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user





