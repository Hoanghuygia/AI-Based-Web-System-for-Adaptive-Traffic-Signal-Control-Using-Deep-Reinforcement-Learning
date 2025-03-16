from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict
from bson.objectid import ObjectId

class DateTimeModelMixin(BaseModel):
    created_at: datetime | None = Field(None, alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")

class DBModelMixin(DateTimeModelMixin):
    id: str | None = None
    # id: ObjectId | None = None
    # created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_config = ConfigDict(arbitrary_types_allowed=True)
