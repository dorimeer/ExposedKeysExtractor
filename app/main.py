import logging
import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from api.api_v1.api import api_router
from core.settings import settings

logger = logging.getLogger(__name__)

app = FastAPI(
    title='Exposed Keys Collector',
    version='0.1',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup():
    random.shuffle(settings.GITHUB_TOKENS)
    obs = models.github.observable
    github_events = models.github.subject
    keys_finders = models.exposed_keys_extractor.subjects
    for key_finder_subject in keys_finders.values():
        await github_events.subscribe_async(key_finder_subject)
    await obs.subscribe_async(github_events)


@app.on_event("shutdown")
async def shutdown():
    pass


@app.get("/health", include_in_schema=False)
async def health():
    return {"message": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
