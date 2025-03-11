from datetime import datetime
from pydantic import BaseModel, Field

class DateTimeModelMixin(BaseModel):
    created_at: datetime | None = Field(None, alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")

class DBModelMixin(DateTimeModelMixin):
    id: int | None = None
