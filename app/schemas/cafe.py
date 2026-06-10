from pydantic import BaseModel
from typing import Optional

class CafeBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class CafeCreate(CafeBase):
    pass

class CafeRead(CafeBase):
    id: int
    owner_id: int
    logo_url: Optional[str] = None

    class Config:
        from_attributes = True