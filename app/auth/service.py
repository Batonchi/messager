from jose import JWTError, jwt
from fastapi import Request, HTTPException
from app.users.service import UserService
from constant import SECRET_KEY, ALGORITHM


def create_token(email: str, password: str):
    data = {"email": email, "password": password}
    token = jwt.encode(data, SECRET_KEY, ALGORITHM)
    return token


def get_user_by_token(request: Request):
    token = request.cookies.get('token')
    if token:
        try:
            data = jwt.decode(token, SECRET_KEY, ALGORITHM)
        except:
            raise HTTPException(status_code=401, detail="Пожалуйста войдите в аккаунт!")
        
        user = UserService.find_by_email_and_password(data['email'], data['password'])
        if not user:
            raise HTTPException(status_code=409, detail="Пользователь не найден! Неверный логин или пароль!")
        return user

