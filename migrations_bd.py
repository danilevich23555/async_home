import asyncio
from sqlalchemy import  Integer, String, Column, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker



engine = create_async_engine('postgresql+asyncpg://app:1234@127.0.0.1:5432/netology', echo=True)
Base = declarative_base()



class Hero(Base):

    __tablename__='herotable'

    id=Column(Integer, primary_key=True)
    birth_year=Column(String(1000), nullable=False)
    eye_color=Column(String(1000), nullable=False)
    films=Column(String(1000), nullable=False)
    gender=Column(String(1000),nullable=False)
    hair_color=Column(String(1000),nullable=False)
    height=Column(String(1000),nullable=False)
    homeworld=Column(String(1000),nullable=False)
    mass=Column(String(1000),nullable=False)
    name=Column(String(1000),nullable=False)
    skin_color=Column(String(1000),nullable=False)
    species=Column(String(1000),nullable=False)
    starships=Column(String(1000),nullable=False)
    vehicles=Column(String(1000),nullable=False)

async def get_async_session(
    drop: bool = False, create: bool = False
):

    async with engine.begin() as conn:
        if drop:
            await conn.run_sync(Base.metadata.drop_all)
        if create:
            print(1)
            await conn.run_sync(Base.metadata.create_all)
    async_session_maker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker


async def main():
    await get_async_session(True, True)

if __name__ == '__main__':
    asyncio.run(main())