from pydantic import BaseModel


# 工具模型


class BaseToDo(BaseModel):
    content: str
    done: bool
    owner_id: int


class ToDo(BaseToDo):
    id: int

    class Config:
        orm_mode = True
