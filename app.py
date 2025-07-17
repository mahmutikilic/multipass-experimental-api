from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from load_credentials import Users
from os_info import OSInfo
from loadconfig import Config, Dotenv
from multipass import list_instances, find_images, launch_instance, get_version
import logg3r

app = FastAPI(title="Multipass Experimental API")

logger = logg3r.setup_logging()
config = Config()
users = Users()


class InstanceConfig(BaseModel):
    name: str | None = None
    cpu: int | None = None
    disk: str | None = None
    mem: str | None = None
    image: str | None = None


@app.get("/")
async def root():
    return {"message": "Multipass API running"}


@app.get("/installable-images")
async def installable_images():
    try:
        return find_images()
    except Exception as exc:
        logger.error(exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/create-instance")
async def create_instance(cfg: InstanceConfig):
    try:
        new_name = launch_instance(cfg.name, cfg.cpu, cfg.disk, cfg.mem, cfg.image)
        return {"name": new_name}
    except Exception as exc:
        logger.error(exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/instances")
async def instances():
    try:
        return list_instances()
    except Exception as exc:
        logger.error(exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/about/{uri}")
async def about(uri: str):
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
