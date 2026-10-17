import json
from typing import  Any
import  redis.asyncio as redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
#创建redis 的连接对象
redis_client = redis.Redis(
    host=REDIS_HOST, # redis服务地址
    port=REDIS_PORT, # redis端口号
    db=REDIS_DB, # 数据库编号 0-15
    decode_responses=True, # 返回结果为字符串类型
    protocol=3
)


#设置 和 读取 （字符串 和 列表 与 字典）"[{}]"
# 封装一个读取缓存 ：字符串
async def get_cache(key:str):
    try:
         return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败：{e}")
        return None

#读取：字典
async def get_json_cache(key:str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data) # 序列化
        return None
    except Exception as e:
        print(f"获取json缓存失败：{e}")


#设置缓存
async  def set_cache(key:str,value:Any,expire:int=3600):
    try:
        if isinstance(value,(dict,list)):
            #转字符串
            value = json.dumps(value,ensure_ascii=False)# 转json,保留中文
        await redis_client.setex(key,expire,value)
        return True
    except Exception as e:
        print(f"设置缓存失败：{e}")
        return False
