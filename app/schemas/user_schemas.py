from pydantic import BaseModel, Field, RootModel
from typing import List, Optional

class CreateUserRequest(BaseModel):
    name: str = Field(max_length=64)
    display_name: str = Field(max_length=64)

class CreateUserResponse(BaseModel):
    id: str

class User(BaseModel):
    name: str
    display_name: str
    creation_time: str

class ListUsersResponse(RootModel[List[User]]):
    pass

class DescribeUserRequest(BaseModel):
    id: str

class DescribeUserResponse(BaseModel):
    name: str
    description: str
    creation_time: str

class UpdateUserPayload(BaseModel):
    name: Optional[str] = Field(default=None, max_length=64)
    display_name: Optional[str] = Field(default=None, max_length=128)

class UpdateUserRequest(BaseModel):
    id: str
    user: UpdateUserPayload

class Team(BaseModel):
    name: str
    description: str
    creation_time: str

class GetUserTeamsRequest(BaseModel):
    id: str

class GetUserTeamsResponse(RootModel[List[Team]]):
    pass
