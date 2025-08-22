import json
from fastapi import APIRouter, Depends

from app.dependencies import get_board_manager
from app.schemas import board_schemas as model
from impl.board_manager import BoardManager

router = APIRouter(prefix="/api/v1/board", tags=["Project Board"])

@router.post("/create", response_model=model.CreateBoardResponse)
def create_board(req: model.CreateBoardRequest, manager: BoardManager = Depends(get_board_manager)):
    res_json = manager.create_board(req.model_dump_json())
    return json.loads(res_json)

@router.post("/close")
def close_board(req: model.CloseBoardRequest, manager: BoardManager = Depends(get_board_manager)):
    res_json = manager.close_board(req.model_dump_json())
    return json.loads(res_json)

@router.post("/add_task", response_model=model.AddTaskResponse)
def add_task(req: model.AddTaskRequest, manager: BoardManager = Depends(get_board_manager)):
    res_json = manager.add_task(req.model_dump_json())
    return json.loads(res_json)

@router.post("/update_task_status")
def update_task_status(req: model.UpdateTaskStatusRequest, manager: BoardManager = Depends(get_board_manager)):
    res_json = manager.update_task_status(req.model_dump_json())
    return json.loads(res_json)

@router.post("/", response_model=model.ListBoardsResponse)
def list_boards(req: model.ListBoardsRequest, manager: BoardManager = Depends(get_board_manager)):
    res_json = manager.list_boards(req.model_dump_json())
    return json.loads(res_json)

@router.post("/export", response_model=model.ExportBoardResponse)
def export_board(req: model.ExportBoardRequest, manager: BoardManager = Depends(get_board_manager)):
    res_json = manager.export_board(req.model_dump_json())
    return json.loads(res_json)
