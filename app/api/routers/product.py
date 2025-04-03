from datetime import datetime
from typing import Sequence, List, Optional, Any, Coroutine
from fastapi import (
    APIRouter,
    Depends,
    Header,
    Query,
    status,
    HTTPException,
    Form,
    File,
    UploadFile,
)
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models.product.product import Product

from app.core.datebases.postgres import get_general_session

