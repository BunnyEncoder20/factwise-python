import json
from fastapi import APIRouter, Depends

from dependencies import get_user_manager
from schemas import CreateUserRequest, CreateUserResponse, ListUsersResponse
from impl.user_manager import UserManager

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create", response_model=CreateUserResponse)
def create_user(req: CreateUserRequest, manager: UserManager = Depends(get_user_manager)):
    response_json = manager.create_user(req.model_dump_json())
    return json.loads(response_json)

@router.get("/list", response_model=ListUsersResponse)
def list_users(manager: UserManager = Depends(get_user_manager)):
    response_json = manager.list_users()
    return json.loads(response_json)
