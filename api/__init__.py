from api.routes.auth import router as auth_router
from api.routes.task import router as task_router
from api.routes.user import router as user_router

__all__ = [
    "auth_router",
    "task_router",
    "user_router",
]