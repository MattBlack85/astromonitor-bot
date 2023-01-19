from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .factory import db_factory

engine = create_async_engine(db_factory(), echo=False)
session = async_sessionmaker(engine)
