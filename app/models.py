import enum
import uuid

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Numeric, func
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class OperationType(enum.Enum):
    """Enum, который представляет типы финансовых операций."""

    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class Wallet(Base):
    """Модель таблицы БД"""

    __tablename__ = "wallets"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    balance = Column(Numeric(15, 2), default=0.00, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    last_operation = Column(SQLEnum(OperationType))
