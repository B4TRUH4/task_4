from datetime import datetime

from sqlalchemy import DateTime, Date
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class TradingResult(Base):
    """Модель результата торгов"""

    __tablename__ = 'spimex_trading_result'
    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str | None]
    exchange_product_name: Mapped[str | None]
    oil_id: Mapped[str | None]
    delivery_basis_id: Mapped[str | None]
    delivery_basis_name: Mapped[str | None]
    delivery_type_id: Mapped[str | None]
    volume: Mapped[int | None]
    total: Mapped[int | None]
    count: Mapped[int | None]
    date: Mapped[datetime.date] = mapped_column(Date)
    created_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_on: Mapped[datetime] = mapped_column(
        DateTime, onupdate=datetime.now, default=datetime.now
    )
