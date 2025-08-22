# Schemas for Team management
from pydantic import BaseModel, Field, RootModel
from typing import List, Optional

class CreateTeamRequest(BaseModel):
    name: str = Field(max_length=64)
    description: Optional[str] = Field(default = None, max_length=128)
    admin: str

class CreateTeamResponse(BaseModel):
    id: str

class TeamInfo(BaseModel):
    name: str
    description: str
    creation_time: str
    admin: str

class ListTeamsResponse(BaseModel):
    RootModel: List[TeamInfo]

class DescribeTeamRequest(BaseModel):
    id: str

class DescribeTeamResponse(BaseModel):
    name: str
    description: str
    creation_time: str
    admin: str

class UpdateTeamPayload(BaseModel):
    name: Optional[str] = Field(max_length=64)
    description: Optional[str] = Field(max_length=128)
    admin: Optional[str] = None

class UpdateTeamRequest(BaseModel):
    id: str
    team: UpdateTeamPayload

class UpdateTeamResponse(BaseModel):
    status: str

class AddUsersToTeamRequest(BaseModel):
    id: str
    users: List[str]

class RemoveUsersFromTeamRequest(BaseModel):
    id: str
    users: List[str]

class TeamUser(BaseModel):
    id: str
    name: str
    display_name: str

class ListTeamUsersRequest(BaseModel):
    id: str

class ListTeamUsersResponse(BaseModel):
    RootModel: List[TeamUser]
