from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from models.news import Category ,News
async  def get_categories(db :AsyncSession ,skip:int=0,limit : int=100 ):
    stmt = select(Category).offset(skip).limit(limit)# 创建查询语句
    result =  await db.execute(stmt)# 执行查询
    return  result.scalars().all()# 返回所有数据

async  def get_news_list(db:AsyncSession,category_id:int,skip:int=0,limit :int = 10):
    #查询指定分类下的所有新闻
    stmt = select(News).where(News.category_id ==  category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return  result.scalars().all()

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
async  def increase_news_views(db:AsyncSession,news_id:int):
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