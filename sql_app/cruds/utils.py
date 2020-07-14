from sqlalchemy.orm import Session

from .. import models
from ..schemas import schemas_utils

'''
# TODO管理
'''


# 根据用户ID获取TODO信息
def get_todo(db: Session, uid: int):
    return db.query(models.ToDo).filter(models.ToDo.owner_id == uid).all()


# 创建TODO信息
def create_todo(db: Session, todo_data: schemas_utils.BaseToDo):
    db_todo = models.ToDo(content=todo_data.content, owner_id=todo_data.owner_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# 删除TODO信息
def delete_todo(db: Session, todo_id: int, uid: int):
    res = db.query(models.ToDo).filter(models.ToDo.id == todo_id, models.ToDo.owner_id == uid).delete()
    db.commit()
    return res


# 修改TODO信息
def update_todo(db: Session, todo_data: schemas_utils.ToDo):
    res = db.query(models.ToDo).filter(models.ToDo.id == todo_data.id).update(todo_data)
    db.commit()
    return res
