from impl.user_manager import UserManager
from impl.team_manager import TeamManager
from impl.board_manager import BoardManager

# Dependency providers
"""
Provides a new instance of Manager.
Later, if you want to switch to a DB instead of JSON, you just update here without touching routers.
"""
def get_user_manager() -> UserManager:
    return UserManager()

def get_team_manager() -> TeamManager:
    return TeamManager()

def get_board_manager() -> BoardManager:
    return BoardManager()
