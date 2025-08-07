from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
import redis.asyncio as redis
from werkzeug.security import check_password_hash

from load_credentials import Users
from os_info import OSInfo
from loadconfig import Config, Dotenv
from multipass import list_instances, find_images, launch_instance, get_version
from prepare import SignalSum
import logg3r

app = FastAPI(title="Multipass Experimental API")
app.mount("/ui", StaticFiles(directory="static", html=True), name="ui")

logger = logg3r.setup_logging()
config = Config()
users = Users()

redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True)

SECRET_KEY = config.SERVER_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/api/login")

api = APIRouter(prefix="/v1/api")


class InstanceConfig(BaseModel):
    name: str | None = None
    cpu: int | None = None
    disk: str | None = None
    mem: str | None = None
    image: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        exists = await redis_client.exists(f"auth_token:{token}")
        if not exists:
            raise HTTPException(status_code=401, detail="Token expired")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/")
async def root():
    return {"message": "Multipass API running"}

app.include_router(api)


@api.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    creds = users.credentials()
    hashed = creds.get(form_data.username)
    if not hashed or not check_password_hash(hashed, form_data.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": form_data.username})
    await redis_client.setex(f"auth_token:{token}", ACCESS_TOKEN_EXPIRE_MINUTES * 60, form_data.username)
    return {"access_token": token, "token_type": "bearer"}


@api.get("/installable-images")
async def installable_images(current_user: str = Depends(get_current_user)):
    try:
        return find_images()
    except Exception as exc:
        logger.error(exc)
        raise HTTPException(status_code=500, detail=str(exc))


@api.post("/create-instance")
async def create_instance(cfg: InstanceConfig, current_user: str = Depends(get_current_user)):
    try:
        new_name = launch_instance(cfg.name, cfg.cpu, cfg.disk, cfg.mem, cfg.image)
        return {"name": new_name}
    except Exception as exc:
        logger.error(exc)
        raise HTTPException(status_code=500, detail=str(exc))


@api.get("/instances")
async def instances(current_user: str = Depends(get_current_user)):
    try:
        return list_instances()
    except Exception as exc:
        logger.error(exc)
        raise HTTPException(status_code=500, detail=str(exc))


@api.get("/status")
async def status(current_user: str = Depends(get_current_user)):
    """Return basic system checks useful before operations."""
    summary = SignalSum()
    return {
        "ready": bool(summary),
        "details": summary.multipass_ok(),
    }


@api.get("/about/{uri}")
async def about(uri: str, current_user: str = Depends(get_current_user)):
    info = OSInfo()
    if uri == "machine-info":
        return info.commoninfo
    if uri == "multipass-status":
        try:
            ver = get_version()
            return {"multipass": ver}
        except Exception:
            raise HTTPException(status_code=503, detail="multipass not available")
    if uri == "multipass-version":
        try:
            return {"version": get_version()}
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))
    if uri == "appversion":
        return Dotenv().appversion()
    raise HTTPException(status_code=404, detail="unknown")


if __name__ == "__main__":
    logger.info("Starting server")
    import uvicorn
    uvicorn.run(
        "app:app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        reload=config.SERVER_DEBUG,
    )
