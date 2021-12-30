from pydantic import BaseModel, Field


class WordSearch(BaseModel):
    words: list[str] = Field(max_length=50)
