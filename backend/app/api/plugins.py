from fastapi import APIRouter

from app.plugins.manager import PluginManager

router = APIRouter(prefix="/plugins")

manager = PluginManager()


@router.get("/system")
def system_info():
    return manager.execute("system")