from datetime import datetime

from sqlmodel import SQLModel, Field
from typing import Optional


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: Optional[int] = Field(default=None, index=True)
    merge_request_iid: Optional[int] = Field(default=None, index=True)
    status: str
    source_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
