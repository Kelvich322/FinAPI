from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models import OperationType


class OperationRequest(BaseModel):
    """Схема для запроса на операцию с кошельком."""

    operation_type: OperationType
    amount: Decimal = Field(ge=0, max_digits=15, decimal_places=2, examples=[0.00])


class OperationResponse(BaseModel):
    """Схема для ответа с результатом операции."""

    id: UUID
    balance: Decimal = Field(ge=0, max_digits=15, decimal_places=2, examples=[0.00])
    last_operation: Optional[OperationType] = None
    amount: Decimal = Field(ge=0, max_digits=15, decimal_places=2, examples=[0.00])

    class Config:
        from_attributes = True


class WalletResponse(BaseModel):
    """Схема информации о кошельке."""

    id: UUID
    balance: Decimal = Field(ge=0, max_digits=15, decimal_places=2, examples=[0.00])
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
