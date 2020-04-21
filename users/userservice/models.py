from sqlalchemy import (
    Column, Integer, VARCHAR
)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine(
        "mysql+pymysql://root:xiang1018@localhost:3306/users?charset=utf8",
        max_overflow=0,  # 超过连接池大小外最多创建的连接
        pool_size=5,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
    )


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(VARCHAR(255), nullable=False)


def init_db():
    Base.metadata.create_all(engine)


init_db()
Session = sessionmaker(bind=engine)
