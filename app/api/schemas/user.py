from decimal import Decimal

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional
from enum import Enum


class CreateUser(BaseModel):
    email: str
    password: str
    full_name: str

class ResponseUser(BaseModel):
    id: int
    email: str
    full_name: str
    is_admin: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Login(BaseModel):
    email: str
    password: str