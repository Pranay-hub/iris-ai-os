from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.plugins import router as plugin_router
from app.api.capabilities import router as capabilities_router


app = FastAPI(title="IRIS Core")

app.include_router(chat_router)
app.include_router(plugin_router)
app.include_router(capabilities_router)
@app.get("/")
def home():
    return {"status": "IRIS backend running"}