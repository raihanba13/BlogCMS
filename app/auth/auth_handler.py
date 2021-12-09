import time 
from typing import Dict 
import jwt 

# this can be used to read env var 
# from decouple import config
# JWT_SECRET = config("secret")
# JWT_ALGO = config("algorithm")

JWT_SECRET = r'12345678'
JWT_ALGO = r'HS256'

def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id, 
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        print(decoded_token)
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        print(e)
        return {}