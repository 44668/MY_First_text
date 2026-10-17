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
