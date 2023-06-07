import bcrypt
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt

from app.api.routes import router as api_router
from app.core import config, tasks
from app.db.repositories.users import UsersRepository
from app.api.dependencies.database import get_repository


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
            import sys
            print(payload, file=sys.stderr)
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


@app.get("/protected_route", dependencies=[Depends(get_current_user)])
async def protected_route():
    return {"message": "Hello!"}


@app.post("/login")
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
