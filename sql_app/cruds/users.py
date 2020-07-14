from sqlalchemy.orm import Session
from .. import models
from passlib.context import CryptContext
from ..schemas import schemas_user

# 数据交互

SECRET_KEY = "wtt"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 获取密码哈希值
def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 根据用户ID获取用户信息
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# 根据 email 获取用户信息
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# 根据用户邮箱和密码获取用户信息
def get_user_by_login(db: Session, email: str, password: str):
    fake_hashed_password = password + SECRET_KEY
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False
    if not verify_password(fake_hashed_password, user.hashed_password):
        return False
    return user


# 获取所有用户信息
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# 创建用户
def create_user(db: Session, user: schemas_user.UserCreate):
    fake_hashed_password = get_password_hash(user.password + SECRET_KEY)
    username = user.email.split('@')[0] if '@' in user.email else user.email
    db_user = models.User(email=user.email, username=username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 删除用户
def delete_user(db: Session, user_id: int):
    res = db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return res


# 修改用户
def update_user(db: Session, user: schemas_user.User):
    user = dict(user)
    uid = user.pop('id')
    user.pop('email')
    res = db.query(models.User).filter(models.User.id == uid).update(user)
    db.commit()
    return res


# 修改用户密码
def update_user_password(db: Session, user: schemas_user.UserPassWord):
    fake_hashed_password = user.oldpassword + SECRET_KEY
    userDb = db.query(models.User).filter(models.User.id == user.id).first()
    if not userDb:
        return False
    if not verify_password(fake_hashed_password, userDb.hashed_password):
        return False
    fake_hashed_password = get_password_hash(user.password + SECRET_KEY)
    res = db.query(models.User).filter(models.User.id == user.id).update({"hashed_password": fake_hashed_password})
    db.commit()
    return res
