from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sql_app import cruds
from sqlalchemy.orm import Session
from sql_app.database import get_db
from sql_app.schemas import schemas_user
from routers.auth import get_current_active_user, role_check

router = APIRouter()

# 创建用户
@router.post("/api/users/", response_model=schemas_user.User)
async def create_user(user: schemas_user.UserCreate, db: Session = Depends(get_db)):
    db_user = cruds.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return cruds.create_user(db=db, user=user)


# 获取所有用户信息(需管理员权限)
@router.get("/api/users/", response_model=List[schemas_user.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     role_res: schemas_user.User = Depends(role_check)):
    users = cruds.get_users(db, skip=skip, limit=limit)
    return users


# 获取本人信息
@router.get("/api/users/me", response_model=schemas_user.User)
async def read_user(db: Session = Depends(get_db), Users: schemas_user.User = Depends(get_current_active_user)):
    db_user = cruds.get_user(db, user_id=Users.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 根据用户ID查询用户信息(非管理员权限只能查询自己的信息)
@router.get("/api/users/{user_id}", response_model=schemas_user.User)
async def read_user(user_id: int, db: Session = Depends(get_db),
                    Users: schemas_user.User = Depends(get_current_active_user)):
    if Users.role != "admin" and Users.id != user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    db_user = cruds.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 根据用户ID删除用户信息(非管理员权限只能删除自己的信息)
@router.delete("/api/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db),
                      Users: schemas_user.User = Depends(get_current_active_user)):
    if Users.role != "admin" and Users.id != user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    res = cruds.delete_user(db, user_id=user_id)
    if res <= 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"msg": "Successfully deleted {} data".format(res)}


# 根据用户ID修改用户信息(非管理员权限只能修改自己的信息)
@router.put("/api/users/")
async def update_user(user: schemas_user.User, db: Session = Depends(get_db),
                      Users: schemas_user.User = Depends(get_current_active_user)):
    if Users.role != "admin" and Users.id != user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    if Users.role != "admin":
        # 只有管理员能修改用户角色
        user.role = "general"
    res = cruds.update_user(db, user=user)
    if res <= 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"msg": "Successfully updated {} data".format(res)}


# 根据用户ID修改用户密码
@router.post("/api/users/password/")
async def update_user_password(user: schemas_user.UserPassWord, db: Session = Depends(get_db),
                      Users: schemas_user.User = Depends(get_current_active_user)):
    if Users.id != user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    res = cruds.update_user_password(db, user=user)
    if res <= 0:
        raise HTTPException(status_code=403, detail="Old password is wrong")
    return {"msg": "Successfully updated {} data".format(res)}
