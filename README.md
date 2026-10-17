# Toutiao Backend - 基于 FastAPI 的新闻资讯后端系统

这是一个使用 FastAPI 构建的高性能异步新闻后端系统。项目采用了标准的分层架构，包含用户认证、新闻浏览、收藏、浏览历史以及 Redis 缓存优化等核心功能。

## 🛠️ 技术栈

*   **Web 框架**: FastAPI
*   **ORM**: SQLAlchemy (Async)
*   **数据库**: MySQL (使用 `aiomysql` 异步驱动)
*   **缓存**: Redis (Windows 下使用 Memurai)
*   **数据校验**: Pydantic v2
*   **认证机制**: UUID Token

## 📂 项目结构

```text
toutiao_backend/
├── cache/              # 缓存模块 (Redis 读写封装)
├── config/             # 配置文件 (数据库、Redis 连接池)
├── crud/               # 数据访问层 (封装具体的数据库操作)
├── models/             # 数据库 ORM 模型 (表结构定义)
├── routers/            # 路由层 (API 接口定义与参数校验)
├── schemas/            # 数据模型层 (Pydantic 请求/响应校验)
├── utils/              # 工具类 (认证、全局异常处理、统一响应封装)
├── .gitignore          # Git 忽略文件配置
├── main.py             # FastAPI 应用入口
└── requirements.txt    # 项目依赖清单
1. 环境准备
请确保你的电脑上已安装以下环境：

Python 3.11+ (推荐使用官方纯净版)

MySQL 8.0+

Redis (Windows 推荐使用 Memurai)

2. 安装依赖
在项目根目录下打开终端，创建并激活虚拟环境（可选但推荐）：

bash
python -m venv venv
# Windows 激活
.\venv\Scripts\activate
# macOS/Linux 激活
# source venv/bin/activate
安装所需的 Python 依赖包：

bash
pip install -r requirements.txt
pip install "redis[hiredis]" -i https://pypi.tuna.tsinghua.edu.cn/simple
3. 配置数据库与缓存
修改 config/db_conf.py 中的 MySQL 数据库连接 URL（请替换为你自己的用户名和密码）。

修改 config/cache_conf.py 中的 Redis 配置（默认连接 localhost:6379）。

4. 启动服务
bash
uvicorn main:app --reload
服务启动后，访问本地接口文档：http://127.0.0.1:8000/docs

📌 核心功能说明
用户模块: 用户注册、登录、Token 认证、获取/修改个人信息、修改密码。

新闻模块:

获取新闻分类（带缓存）。

分页获取新闻列表（带缓存）。

获取新闻详情及浏览量自增。

获取相关推荐新闻。

收藏模块: 添加收藏、取消收藏、检查收藏状态、分页获取收藏列表。

历史模块: 记录浏览历史、分页获取历史列表、删除/清空历史记录。

全局异常处理: 统一捕获 SQLAlchemy 异常、HTTP 异常以及未知异常，并以标准化 JSON 格式返回。
