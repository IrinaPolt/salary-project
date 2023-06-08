import json
import httpx
import bcrypt
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt

from app.api.routes import router as api_router
from app.core import config, tasks
from app.db.repositories.users import UsersRepository
from app.models.users import UserInfo
from app.api.dependencies.database import get_repository

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR / 'utils'

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
SECRET_KEY = str(config.SECRET_KEY)


app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


@app.on_event("startup")
async def startup():
    await tasks.create_start_app_handler(app)()


@app.on_event("shutdown")
async def shutdown():
    await tasks.create_stop_app_handler(app)()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return email


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/check/", dependencies=[Depends(get_current_user)], name="users:check", status_code=HTTP_200_OK)
async def protected_route(
        email: str = Depends(get_current_user),
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserInfo:
    user = await users_repo.get_user_info(email=email)
    return user


@app.post("/login/", name="users:login", status_code=HTTP_200_OK)
async def login(
        email: str,
        password: str,
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
        ):
    user = await users_repo.get_user_by_email(email=email)
    hashed_password = user.password_hash

    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        access_token = create_access_token(
            data={"email": email},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        return {"error": "Invalid username or password"}


def load_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


@app.get("/load_data/", status_code=HTTP_201_CREATED)
async def load():
    users_data = load_from_file(PROJECT_DIR / 'users.json')
    wages_data = load_from_file(PROJECT_DIR / 'wages.json')
    promotions_data = load_from_file(PROJECT_DIR / 'promotions.json')
    async with httpx.AsyncClient() as client:
        for user_data in users_data:
            response = await client.post("http://localhost:8000/api/users/", json={"new_user": user_data})
            if response.status_code == 201:
                continue
            else:
                return f"Failed to create user: {response.text}"
        for wage_data in wages_data:
            response = await client.post("http://localhost:8000/api/wages/", json={"new_wage": wage_data})
            if response.status_code == 201:
                continue
            else:
                return f"Failed to create user's wage: {response.text}"
        for promotion_data in promotions_data:
            response = await client.post("http://localhost:8000/api/promotions/",
                                         json={"new_promotion": promotion_data})
            if response.status_code == 201:
                continue
            else:
                return f"Failed to create user's promotion: {response.text}"
            return "Data loaded successfully"
