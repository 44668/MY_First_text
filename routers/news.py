
from fastapi import APIRouter, Depends, Query, HTTPException
from crud import news, news_cache
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession
"""
接口实现流程
1.模块化路由 -> API接口规范文档
2.定义模型类 -> 数据库表（数据库设计文档）
3.在crud文件里创建文件，封装操作数据库的方法
4.在路由处理函数里面调用crud封装好的方法，响应结果
"""

#创建APIRouter实例
router = APIRouter(prefix="/api/news",tags=["news"])

@router.get("/categories")
async  def get_categories(skip:int=0,limit:int=100,db:AsyncSession=Depends(get_db)):
    categories = await news_cache.get_categories(db,skip,limit)
    return {"code":200,
            "message":"获取新闻分类成功。",
            "data":categories}

@router.get("/list")
async  def get_news_list(
        category_id: int = Query(..., alias="categoryId"),
        page:int = 1,
        page_size :int = Query(10,alias="pageSize",le=100), # 限制page_size最大值为100
        db:AsyncSession=Depends(get_db)
):
    #思路:处理分页规则 ->查询新闻列表->计算总量 ->计算是否还有更多
    offset = (page-1) *page_size
    news_list =  await news_cache.get_news_list(db,category_id,offset,page_size)
    total = await news.get_news_count(db,category_id)
    has_more = (offset+len(news_list)) < total
    return {
        "code" :200,
        "message":"获取新闻列表成功",
        "data":{
            "list":news_list,
            "total":total,
            "hasMore":has_more
        }
    }

@router.get("/detail")
async  def get_news_detail(news_id:int=Query(...,alias="id"),db:AsyncSession=Depends(get_db)):
    #获取新闻详情+浏览量+1+相关新闻
    news_detail = await news.get_news_detail(db,news_id)
    if not news_detail:
        raise HTTPException(status_code=404,detail="新闻不存在")

    views_res = await news.increase_mews_views(db,news_detail.id)
    if not views_res:
        raise HTTPException(status_code=404,detail="更新新闻浏览量失败")

    related_news = await news.get_related_news(db,news_detail.id,news_detail.category_id)
    return {
        "code":200,
        "message":"获取新闻详情成功",
        "data":{
            "id":news_detail.id,
            "title":news_detail.title,
            "content":news_detail.content,
            "image":news_detail.image,
            "author":news_detail.author,
            "publishedTime":news_detail.publish_time.isoformat(),
            "categoryId":news_detail.category_id,
            "views":news_detail.views,
            "relatedNews":related_news
        }
    }