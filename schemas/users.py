from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class UserRequest(BaseModel):
    username : str
    password : str

# 用户信息基础数据模型
class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")


class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True  # 允许从 ORM 对象属性中取值
    )


#data 数据类型
class UserAuthResponse(BaseModel):
    token:str
    user_info:UserInfoResponse = Field(...,alias="userInfo")

    #模型类的配置
    model_config = ConfigDict(
        populate_by_name= True, # 字段名映射属性
        from_attributes=True  # 从属性映射字段 ,允许从orm 对象属性中取值
    )

#更新用户信息的模型类
class UserUpdateRequest(BaseModel):
    nickname:str =None
    avatar:str =None
    gender:str =None
    bio:str =None
    phone:str =None

class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(...,alias='oldPassword',description="旧密码")
    new_password: str = Field(...,min_length=6,alias='newPassword',description="新密码")


