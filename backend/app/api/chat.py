from fastapi import APIRouter
from app.llm.router import IRISRouter

router = APIRouter()
iris = IRISRouter()


@router.post("/chat")
def chat(payload: dict):
    message = payload.get("message")
    mode = payload.get("mode", "auto")

    response = iris.run(message, mode)

    return {
        "response": response,
        "mode": mode
    }