import logging

from fastapi import APIRouter
from starlette.responses import StreamingResponse

import models
import schemas
from models import utils

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get('/raw')
async def recent_changes():
    return StreamingResponse(utils.json_stream_from_observable(models.github.subject))


@router.get('/exposed_keys')
async def recent_changes(data: schemas.WordSearch):
    subj = await models.exposed_keys_extractor.observable_from_several_words(data.words)
    return StreamingResponse(utils.json_stream_from_observable(subj))
