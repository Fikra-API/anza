from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

load_dotenv()

from app.db import init_db, create_user, get_user_by_email, get_user_by_id
from app.auth import (
    hash_password,
    verify_password,
    create_session_token,
    read_session_token,
    COOKIE_NAME,
)
from app.ai import generate_chat_reply


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Anza", lifespan=lifespan)


class AuthPayload(BaseModel):
    email: str
    password: str


class ChatPayload(BaseModel):
    message: str


def get_current_user(request: Request):
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    user_id = read_session_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


@app.post("/api/signup")
def signup(payload: AuthPayload, response: Response):
    email = payload.email.strip().lower()
    if not email or not payload.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required",
        )
    if get_user_by_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    password_hash, salt = hash_password(payload.password)
    user_id = create_user(email, password_hash, salt)

    token = create_session_token(user_id)
    response.set_cookie(key=COOKIE_NAME, value=token, httponly=True, samesite="lax")
    return {"ok": True, "user": {"id": user_id, "email": email}}


@app.post("/api/login")
def login(payload: AuthPayload, response: Response):
    email = payload.email.strip().lower()
    user = get_user_by_email(email)
    if not user or not verify_password(payload.password, user["password_hash"], user["salt"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_session_token(user["id"])
    response.set_cookie(key=COOKIE_NAME, value=token, httponly=True, samesite="lax")
    return {"ok": True, "user": {"id": user["id"], "email": user["email"]}}


@app.post("/api/logout")
def logout(response: Response):
    response.delete_cookie(key=COOKIE_NAME)
    return {"ok": True}


@app.get("/api/me")
def me(request: Request):
    user = get_current_user(request)
    return {"ok": True, "user": {"id": user["id"], "email": user["email"]}}


@app.post("/api/chat")
def chat_post(payload: ChatPayload, request: Request):
    get_current_user(request)
    message = payload.message.strip()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty",
        )
    try:
        reply = generate_chat_reply(message)
        return {"reply": reply}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI service error: {exc}",
        )



app.mount("/", StaticFiles(directory="static", html=True), name="static")
