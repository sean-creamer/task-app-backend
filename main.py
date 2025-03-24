from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import auth_router, task_router, user_router

app = FastAPI()

# Define a CORS policy for your frontend (allow requests from localhost:4200)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
