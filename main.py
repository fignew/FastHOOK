from typing import Optional
from fastapi import FastAPI
from pathlib import Path, PurePath

app = FastAPI()


@app.get("/")
async def read_root():
    return "Howdy"


@app.post("/github/{target}/{hook}")
async def read_github(target: str, hook: str, github_payload: Optional[str] = None):
    """
    Github webhook handler
    """
    hookpath = Path(PurePath("/tmp/github").joinpath(target, hook))
    if hookpath.is_relative_to(PurePath("/tmp/github")):
        hookpath.parent.mkdir(parents=True, exist_ok=True)
        hookpath.touch()
    return {"github_payload": github_payload}
