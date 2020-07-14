from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sql_app import cruds
from sqlalchemy.orm import Session
from sql_app.database import get_db
from routers.auth import role_check
from sql_app.schemas import schemas_utils, schemas_user

router = APIRouter()
'''
# 用户TODO管理
'''


# 新增TODO
@router.post("/api/todo/")
async def create_todo(todo_data: schemas_utils.BaseToDo, db: Session = Depends(get_db),
                      role_res: schemas_user.User = Depends(role_check)):
    if role_res.id != todo_data.owner_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    return cruds.create_todo(db=db, todo_data=todo_data)


# 根据用户ID获取TODO
@router.get("/api/todo/", response_model=List[schemas_utils.ToDo])
async def create_todo(db: Session = Depends(get_db), role_res: schemas_user.User = Depends(role_check)):
    db_todo = cruds.get_todo(db, uid=role_res.id)
    return db_todo


# 根据ID删除TODO
@router.delete("/api/todo/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db),
                      role_res: schemas_user.User = Depends(role_check)):
    res = cruds.delete_todo(db, todo_id=todo_id, uid=role_res.id)
    if res <= 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"msg": "Successfully deleted {} data".format(res)}


# 根据ID修改TODO信息
@router.put("/api/todo/")
async def update_todo(todo_data: schemas_utils.ToDo, db: Session = Depends(get_db),
                      role_res: schemas_user.User = Depends(role_check)):
    if role_res.id != todo_data.owner_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    res = cruds.update_todo(db, todo_data=todo_data)
    if res <= 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"msg": "Successfully updated {} data".format(res)}
