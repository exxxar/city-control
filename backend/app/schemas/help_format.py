from pydantic import BaseModel

class HelpFormatRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True