# Schemas for Project Board management
from pydantic import BaseModel, Field, RootModel
from typing import List, Optional
from enum import Enum

class CreateBoardRequest(BaseModel):
    name: str = Field(max_length=64)
    description: Optional[str] = Field(max_length=128)
    team_id: str

class CreateBoardResponse(BaseModel):
    id: str

class CloseBoardRequest(BaseModel):
    id: str

class AddTaskRequest(BaseModel):
    bid: str = Field(alias="board_id")
    title: str = Field(max_length=64)
    description: Optional[str] = Field(max_length=128)
    user_id: str

class AddTaskResponse(BaseModel):
    id: str

class TaskStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"

class UpdateTaskStatusRequest(BaseModel):
    id: str
    status: TaskStatus

class ListBoardsRequest(BaseModel):
    id: str

class Board(BaseModel):
    id: str
    name: str

class ListBoardsResponse(RootModel[List[Board]]):
    pass

class ExportBoardRequest(BaseModel):
    id: str

class ExportBoardResponse(BaseModel):
    out_file: str
