from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_wallet_operation, get_wallet
from app.database import get_db
from app.models import Wallet
from app.schemas import OperationRequest, OperationResponse, WalletResponse

wallet_router = APIRouter(prefix="/api/v1")


@wallet_router.post(
    "/wallets/{wallet_id}/operation",
    response_model=OperationResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"description": "Wallet not found"},
        400: {"description": "Insufficient funds"},
    },
)
async def create_operation(
    wallet_id: UUID, operation: OperationRequest, db: AsyncSession = Depends(get_db)
):
    """
    Эндпоинт для операции с кошельком по его UUID.

    Принимает JSON формата:

    {
        operation_type: “DEPOSIT” or “WITHDRAW”,
        amount: 1000
    },

    где “DEPOSIT” - операция пополнения средств, “WITHDRAW” - операция списания средств, а amount - количество у.е. для операции.

    """
    return await create_wallet_operation(db, wallet_id, operation)


@wallet_router.get(
    "/wallets/{wallet_id}",
    response_model=WalletResponse,
    responses={404: {"description": "Wallet not found"}},
)
async def get_wallet_balance(wallet_id: UUID, db: AsyncSession = Depends(get_db)):
    """Эндпоинт для получения данных о кошельке по его UUID."""
    wallet = await get_wallet(db, wallet_id)
    return wallet


@wallet_router.post(
    "/wallets",
    response_model=WalletResponse,
    status_code=status.HTTP_201_CREATED,
    responses={404: {"description": "Wallet not found"}},
)
async def create_wallet(db: AsyncSession = Depends(get_db)):
    """Эндпоинт для создания нового кошелька."""
    wallet = Wallet()
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)

    return wallet
