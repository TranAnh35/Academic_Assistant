from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.websocket_endpoint import router as websocket_router
from api.http_endpoint import router as http_router

app = FastAPI(title="Academic Assistant System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow requests from the frontend (default Vite port)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(websocket_router, prefix="/ws", tags=["WebSocket"])
app.include_router(http_router, prefix="/http", tags=["HTTP"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Academic Assistant System"}