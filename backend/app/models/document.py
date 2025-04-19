# models/document.py
from pydantic import BaseModel, Field
from typing import List

class Document(BaseModel):
    title: str = Field(..., description="Title of the academic paper.")
    authors: List[str] = Field(default_factory=list, description="List of authors.")
    year: str = Field(..., description="Publication year (as string).")
    abstract: str = Field(..., description="Abstract or summary of the paper.")
    url: str = Field(..., description="URL link to the paper (if available).")