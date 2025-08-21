import json
from fastapi import APIRouter, Depends

from dependencies import get_user_manager
from schemas import user_schemas as model
from impl.user_manager import UserManager

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create", response_model=model.CreateUserRequest)
def create_user(req: model.CreateUserRequest, manager: UserManager = Depends(get_user_manager)):
    response_json = manager.create_user(req.model_dump_json())
    return json.loads(response_json)

@router.get("/", response_model=model.ListUsersResponse)
def list_users(manager: UserManager = Depends(get_user_manager)):
    response_json = manager.list_users()
    return json.loads(response_json)

@router.get("/describe", response_model=model.DescribeUserResponse)
def describe_user(req: model.DescribeUserRequest, manager: UserManager = Depends(get_user_manager)):
    response_json = manager.describe_user(req.model_dump_json())
    return json.loads(response_json)

@router.post("/update")
def update_user(req: model.UpdateUserRequest, manager: UserManager = Depends(get_user_manager)):
    response_json = manager.update_user(req.model_dump_json())
    return json.loads(response_json)

@router.get("/get_teams", response_model=model.GetUserTeamsResponse)
def get_user_teams(req: model.GetUserTeamsRequest, manager: UserManager = Depends(get_user_manager)):
    response_json = manager.get_user_teams(req.model_dump_json())
    return json.loads(response_json)
