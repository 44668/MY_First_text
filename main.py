from fastapi import FastAPI
from routers import news, users, favorite, history
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handlers import register_exception_handler

app = FastAPI()

# 注册异常处理
register_exception_handler(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 设置允许的源 ,生产环境需要指定。
    allow_credentials=True, # 设置允许携带cookie
    allow_methods=["*"],  # 设置允许的请求方法
    allow_headers=["*"], # 设置允许的请求头
)
@app.get("/")
async def root():
    return {"message": "Hello World"}
#注册路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)