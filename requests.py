from sqlalchemy import Select, update, delete, func
from models import async_session, User, Transaction, Category, AIRequest
from pydantic import BaseModel, ConfigDict
from typing import List
    

class TransactionScheme(BaseModel):
    id: int
    user_id: int
    category_id: int
    amount: float
    description: str | None
    transition_datetime: str
    create_at: str

    model_config = ConfigDict(from_attributes=True)


async def add_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(Select(User).where(User.tg_id == tg_id))
        if user:
            return user
        
        new_user = User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    

async def get_transactions_by_user(user_id: int) -> List[TransactionScheme]:
    async with async_session() as session:
    
        result = await session.scalars(
            Select(Transaction).where(Transaction.user_id == user_id)
        )
        transactions = result.all()

        return [TransactionScheme.model_validate(tx) for tx in transactions]
    

async def get_transaction_count(user_id: int) -> int:
    async with async_session() as session:
        count = await session.scalar(
            Select(func.count()).select_from(Transaction).where(Transaction.user_id == user_id)
        )
        return count