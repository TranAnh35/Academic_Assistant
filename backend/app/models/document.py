from pydantic import BaseModel
from typing import List

class Document(BaseModel):
    title: str
    authors: List[str]
    year: str
    abstract: str
    url: str