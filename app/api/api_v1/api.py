from fastapi import APIRouter

from .endpoints import github

api_router = APIRouter()
api_router.include_router(github.router, prefix='/github', tags=['github'])
