from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def get_wallet(db: AsyncSession, wallet_id: UUID) -> models.Wallet:
    """Получение кошелька из БД."""
    query = select(models.Wallet).where(models.Wallet.id == wallet_id)
    result = await db.execute(query)
    wallet = result.scalar_one_or_none()

    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found"
        )
    return wallet


async def create_wallet_operation(
    db: AsyncSession, wallet_id: UUID, operation: schemas.OperationRequest
) -> schemas.OperationResponse:
    """Произведение транзакции БД с указанной операцией."""
    async with db.begin():
        result = await db.execute(
            select(models.Wallet).where(models.Wallet.id == wallet_id).with_for_update()
        )
        wallet = result.scalar_one_or_none()

        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found"
            )

        if (
            operation.operation_type == models.OperationType.WITHDRAW
            and wallet.balance < operation.amount
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds"
            )

        if operation.operation_type == models.OperationType.DEPOSIT:
            new_balance = wallet.balance + operation.amount
        else:
            new_balance = wallet.balance - operation.amount

        await db.execute(
            update(models.Wallet)
            .where(models.Wallet.id == wallet_id)
            .values(balance=new_balance, last_operation=operation.operation_type)
        )

    return schemas.OperationResponse(
        id=wallet_id,
        balance=new_balance,
        last_operation=operation.operation_type,
        amount=operation.amount,
    )
