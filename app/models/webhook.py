from pydantic import BaseModel, Field
from typing import Optional, List


class User(BaseModel):
    id: int
    name: str
    username: str
    avatar_url: str
    email: str


class Project(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    web_url: str
    avatar_url: Optional[str] = None
    git_ssh_url: str
    git_http_url: str
    namespace: str
    visibility_level: int
    path_with_namespace: str
    default_branch: str
    url: str
    ssh_url: str
    http_url: str


class ObjectAttributes(BaseModel):
    assignee_id: Optional[int] = None
    author_id: int
    created_at: str
    id: int
    iid: int
    source_branch: str
    target_branch: str
    title: str
    state: str
    url: str


class MergeRequestEvent(BaseModel):
    object_kind: str = Field(..., alias='object_kind')
    event_type: str = Field(..., alias='event_type')
    user: User
    project: Project
    object_attributes: ObjectAttributes
