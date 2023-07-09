from pathlib import Path, PurePath

from fastapi import FastAPI
from starlette.requests import Request

app = FastAPI()

# HOOK_DIR /run/fasthook is created by systemd via the RuntimeDirectory option. It's deleted when the service stops.
HOOK_DIR = PurePath("/run/fasthook")

DECODE_FORMAT = "latin-1"


@app.get("/")
async def read_root():
    return "Howdy"


@app.post("/github/{target}/{hook}")
async def read_github(target: str, hook: str):
    """
    Github webhook handler
    """
    hookpath = Path(HOOK_DIR.joinpath(target, hook))
    if hookpath.is_relative_to(HOOK_DIR):
        hookpath.parent.mkdir(parents=False, exist_ok=True)
        hookpath.touch()
        return {"github_payload": "ok"}
    else:
        return {"github_payload": "error"}


@app.middleware("http")
async def case_sens_middleware(request: Request, call_next):
    """
    Make url lowercase
    """
    raw_query_str = request.scope["query_string"].decode(DECODE_FORMAT).lower()
    request.scope["query_string"] = raw_query_str.encode(DECODE_FORMAT)

    path = request.scope["path"].lower()
    request.scope["path"] = path

    response = await call_next(request)
    return response
