from sqlalchemy import ForeignKey, String, BigInteger, DateTime, Float
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///finai.db", echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[String | None] = mapped_column(String(32), unique=True)
    first_name: Mapped[String | None] = mapped_column(String(64))
    last_name: Mapped[String | None] = mapped_column(String(64))
    phone: Mapped[String | None] = mapped_column(String(17))
    create_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[String] = mapped_column(String(64), nullable=False)
    type: Mapped[String] = mapped_column(String(10), nullable=False)  # e.g., 'income' or 'expense'
    icon_name: Mapped[String | None] = mapped_column(String(64))
    color_hex: Mapped[String | None] = mapped_column(String(7))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    amount: Mapped[Float] = mapped_column(Float, nullable=False)
    description: Mapped[String | None] = mapped_column(String(256))
    transition_datetime: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    create_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)


class AIRequest(Base):
    __tablename__ = "ai_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    question: Mapped[String] = mapped_column(String(1024), nullable=False)
    response: Mapped[String | None] = mapped_column(String(2048))
    input_tokens: Mapped[int] = mapped_column(nullable=False)
    output_tokens: Mapped[int] = mapped_column(nullable=False)
    total_tokens: Mapped[int] = mapped_column(nullable=False)
    create_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)