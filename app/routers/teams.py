import json
from fastapi import APIRouter, Depends

from dependencies import get_team_manager
from schemas import team_schemas as model
from impl.team_manager import TeamManager

router = APIRouter(prefix="/team", tags=["Teams"])

@router.post("/create", response_model=model.CreateTeamResponse)
def create_team(req: model.CreateTeamRequest, manager: TeamManager = Depends(get_team_manager)):
    res_json = manager.create_team(req.model_dump_json())
    return json.loads(res_json)

@router.get("/", response_model=model.ListTeamsResponse)
def list_teams(manager: TeamManager = Depends(get_team_manager)):
    res_json = manager.list_teams()
    return json.loads(res_json)

@router.get("/describe", response_model=model.DescribeTeamRequest)
def describe_team(req: model.DescribeTeamRequest, manager: TeamManager = Depends(get_team_manager)):
    res_json = manager.describe_team(req.model_dump_json())
    return json.loads(res_json)

@router.post("/update", response_model=model.UpdateTeamResponse)
def update_team(req: model.UpdateTeamRequest, manager: TeamManager = Depends(get_team_manager)):
    res_json = manager.update_team(req.model_dump_json())
    return json.loads(res_json)

@router.post("/add_to_team")
def add_users_to_team(req: model.AddUsersToTeamRequest, manager: TeamManager = Depends(get_team_manager)):
    res_json = manager.add_users_to_team(req.model_dump_json())
    return json.loads(res_json)

@router.post("/remove_from_team")
def remove_users_from_team(req: model.RemoveUsersFromTeamRequest, manager: TeamManager = Depends(get_team_manager)):
    res_json = manager.remove_users_from_team(req.model_dump_json())
    return json.loads(res_json)

@router.get("/members", response_model=model.ListTeamUsersResponse)
def list_team_users(req: model.ListTeamUsersRequest, manager: TeamManager = Depends(get_team_manager)):
    res_json = manager.list_team_users(req.model_dump_json())
    return json.loads(res_json)
