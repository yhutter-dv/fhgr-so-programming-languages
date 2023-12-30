from pydantic import BaseModel

class GitRepoRequest(BaseModel):
    language: str
