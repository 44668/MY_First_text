#根据用户名查询数据库
import uuid
from datetime import datetime
from fastapi import HTTPException
from future.backports.datetime import timedelta
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
from utils import  security

# 根据用户名查询用户
async def get_user_by_username(db:AsyncSession,username:str):
    query = select(User).where(User.username == username)
    result =await db.execute(query)
    return result.scalar_one_or_none()

#创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 1. 密码加密
    hashed_password = security.get_hash_password(user_data.password)
    # 2. 创建用户对象
    user = User(username=user_data.username, password=hashed_password)
    # 3. 把用户添加到会话中
    db.add(user)
    # 4. 提交事务
    await db.commit()
    # 5. 移除 refresh，避免报错；如果需要用户信息，可以直接用 user 对象
    await db.refresh(user)
    return user

"""
创建token
"""
async  def create_token(db: AsyncSession, user_id: int):
    #生成token +设置过期时间->查询数据库当前用户是否有token ->有：更新；没有：添加
    token = str(uuid.uuid4())
    expire_at = datetime.now() + timedelta(days=7) #设置过期时间
    query = select(UserToken).where(UserToken.user_id == user_id) #查询当前用户
    result = await db.execute(query)
    user_token =result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expire_at
    else:
        user_token = UserToken(user_id=user_id,token=token,expires_at=expire_at)
        db.add(user_token)
        await db.commit()
    return token

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await  get_user_by_username(db,username)
    if not user:
        return None
    if not security.verify_password(password, user.password): #验证密码
        return None
    return  user


#根据token 查询用户 ：验证token->查询用户
async  def get_user_by_token(db: AsyncSession, token: str):
    query= select(UserToken).where(UserToken.token == token)
    result = await  db.execute(query)
    db_token = result.scalar_one_or_none()
    if not db_token or db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await  db.execute(query)
    return  result.scalar_one_or_none()


#更新用户信息
async def update_user(db: AsyncSession, username:str, user_data: UserUpdateRequest):
    #user_date 是一个pydantic类型 ，得到字典 -> **解包
    #没有设置的值不更新（不然未修改的值也会返回NULL）
    query =  update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none =True
     ))
    result = await  db.execute(query)
    await  db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404,detail="用户不存在")

    updated_user = await get_user_by_username(db,username)
    return updated_user

#修改密码 : 验证旧密码 ->新密码加密 -> 修改密码
async def change_password(db:AsyncSession , user:User ,old_password:str,new_password:str):
    if not  security.verify_password(old_password,user.password):
        return False
    hashed_new = security.get_hash_password(new_password)
    user.password = hashed_new
    db.add(user) #添加到会话中 ,由SQLAlchemy 真正接管 USer
    #规避 session 过期 或关闭导致的不能提交问题
    await db.commit()
    await db.refresh(user)
    return True