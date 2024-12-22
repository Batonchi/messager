from jose import JWTError, jwt
from fastapi import Request, HTTPException
from app.users.service import UserService
import hashlib
from constant import SECRET_KEY, ALGORITHM


def create_token(email: str, password: str):
    data = {"email": email, "password": password}
    token = jwt.encode(data, SECRET_KEY, ALGORITHM)
    return token


def hash_password(password: str):
    alg = hashlib.sha256()
    alg.update(password.encode())
    return alg.hexdigest()


def get_user_by_token(request: Request):
    token = request.cookies.get('token')
    if not token: 
        raise HTTPException(status_code=403, detail="Пожалуйста войдите в аккаунт!")
    try:
        data = jwt.decode(token, SECRET_KEY, ALGORITHM)
    except Exception:
        raise HTTPException(status_code=403, detail="Пожалуйста войдите в аккаунт!")
    user = UserService.find_by_email_and_password(data['email'], hash_password(data['password']))
    if not user:
        raise HTTPException(status_code=409, detail="Пользователь не найден! Неверный логин или пароль!")
    return user
    
