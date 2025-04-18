from fastapi import APIRouter, HTTPException, status
from src.auth.oauth2 import create_access_token
from src.config import settings
from pydantic import BaseModel

router = APIRouter(tags=["auth"])


class TokenRequest(BaseModel):
    client_id: str
    client_secret: str


@router.post("/token")
async def login_for_access_token(form: TokenRequest):
    client_id, client_secret = form.client_id, form.client_secret
    if client_id != settings.CLIENT_ID or client_secret != settings.CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect client credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": client_id})
    return {"access_token": access_token, "token_type": "Bearer"}
