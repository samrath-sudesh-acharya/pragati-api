from jose import JWTError, jwt
from fastapi import HTTPException, Security,status,Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

    SECRET_KEY = 'dkhfjeih3hr8o19rjeo832ohjo2e84ojfipwjf92jiognio34jgiojfio32jfoj3ifoh3iofh'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self,plain_password,hashed_password):
        return self.pwd_context.verify(plain_password,hashed_password)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=30),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        jwt_token = jwt.encode(payload,self.SECRET_KEY,algorithm='HS256')
        return jwt_token

    def decode_token(self,token):
        try:
            payload = jwt.decode(token,self.SECRET_KEY,algorithms=["HS256"])
            return payload['sub']
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)

    def auth_wrapper(self,auth : HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
