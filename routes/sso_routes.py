from fastapi import APIRouter, Request, Depends, Response, status, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from config.template import templates
from firebase_admin import auth
from services.dependencies import get_user_token
import services.firebase

sso = APIRouter()

@sso.post("/signin", response_class=Jinja2Templates)
async def signin(request: Request, response: Response, token : str = Body()):
    try:
        decoded_token = auth.verify_id_token(token)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication from Firebase. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )

    return templates.TemplateResponse("index.jinja", {"request": request})

@sso.get("/signout", response_class=Jinja2Templates)
async def signout(request: Request, res: Response, user = Depends(get_user_token)):
    auth.revoke_refresh_tokens(user['uid'])
    
    res = RedirectResponse(url='/', status_code=302)
    res.delete_cookie("token", path="/") 

    return res
