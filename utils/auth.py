
from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud import  users
from config.db_conf import get_db
from starlette import status

# 整合 根据TOKEN 查询用户 ，返回用户
async def get_current_user(
        authorization: str = Header(...,alias="Authorization"),
        db: AsyncSession = Depends(get_db)
):
        token = authorization.replace("Bearer ","")
        user = await  users.get_user_by_token(db, token)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="认证失败，无效的令牌")

        return user
