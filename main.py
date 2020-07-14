import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from sql_app import models
from sql_app.database import engine
from routers import auth, users, utils

# 建表
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(utils.router)

# 跨域配置
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
