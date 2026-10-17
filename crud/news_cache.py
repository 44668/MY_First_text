from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update

from cache.news_cache import get_cached_categories, set_cache_categories, get_cache_news_list, set_cache_news_list
from models.news import Category ,News
from schemas.base import NewsItemBase


async  def get_categories(db :AsyncSession ,skip:int=0,limit : int=100 ):
    #先尝试从缓存中获取数据
    cache_categories = await get_cached_categories()
    if cache_categories:
        return cache_categories
    stmt = select(Category).offset(skip).limit(limit)# 创建查询语句
    result =  await db.execute(stmt)# 执行查询
    categories = result.scalars().all()# 返回所有数据

    #写入缓存
    if categories:
        categories = jsonable_encoder(categories)
        await set_cache_categories(categories)
    #返回
    return  categories

async  def get_news_list(db:AsyncSession,category_id:int,skip:int=0,limit :int = 10):
    #先尝试从缓存获取新闻
    page = skip // limit +1
    cached_list = await  get_cache_news_list(category_id,page,limit)
    if cached_list:
        return  [News(**item) for item in cached_list]
    #查询指定分类下的所有新闻
    stmt = select(News).where(News.category_id ==  category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list =  result.scalars().all()
    #写入缓存
    if news_list :
        #先把orm 数据转换为 pydentic ,再转为字典
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json",by_alias=False) for item in news_list]
        await  set_cache_news_list(category_id,page,limit,news_data)

    return  news_list

async  def get_news_count(
        db:AsyncSession,
        category_id:int
):
    #查询指定分类下的新闻数量
    stmt = select(func.count(News.id)).where(News.category_id ==  category_id)
    result = await db.execute(stmt)
    return  result.scalar_one() #只能有一个结果,否则报错

async  def get_news_detail(db:AsyncSession,news_id:int):
    stmt = select(News).where(News.id ==  news_id)
    result = await db.execute(stmt)
    return  result.scalar_one_or_none() #返回一个结果或者None,能查就返回，查不到就None

# 浏览量+1
async  def increase_mews_views(db:AsyncSession,news_id:int):
    stmt =  update(News).where(News.id == news_id).values(views=News.views+1)
    result = await db.execute(stmt)
    await db.commit()

    #更新->检查数据库是否命中了数据 ->命中返回True
    return result.rowcount > 0
# 相关新闻
async def get_related_news(db: AsyncSession,news_id: int,category_id: int,limit : int = 5):
    #order_by 排序->浏览量和发布时间
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(News.views.desc(),News.publish_time.desc()).limit(limit)
    result = await db.execute(stmt)
    #return result.scalars().all()
    related_news = result.scalars().all()
    #用列表推导式 推导出新闻的核心数据，然后在return
    return [ {
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time.isoformat(),
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
    } for news_detail in related_news]