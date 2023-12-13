from fastapi import Request, Depends, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from firebase_admin import credentials, auth

def formdata_to_json(formdata):
    json_data = {}
    for key, value in formdata.items():
        if key == "file":
            continue
        json_data[key] = value  # Assuming values are bytes and need to be decoded
    return json_data

def get_cookie(request: Request):
    cookies = request.cookies

    token = cookies.get("token")

    return token

def get_user_token_ignore(res: Response, token: str = Depends(get_cookie)):
    if token is None:
        return None
    try:
        decoded_token = auth.verify_id_token(token, check_revoked=True)
    except Exception as err:
        return None
    return decoded_token

# get token from cookie
def get_user_token(res: Response, token: str = Depends(get_cookie)):
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication is needed",
            headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
        )
    try:
        decoded_token = auth.verify_id_token(token, check_revoked=True)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication from Firebase. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
    return decoded_token