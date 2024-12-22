from sqlalchemy import UUID, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from app.configs.database.sqlalchemy_base import Base
from app.models.base_types.base import id_pk, created_at, updated_at
from app.models.enums.bet.status import BetStatus


class Bet(Base):
    __tablename__ = "bets"

    id: Mapped[id_pk]
    event_id: Mapped[UUID] = mapped_column(UUID, nullable=False, comment='Id события')
    amount: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=False, comment='Сумма ставки')
    status: Mapped[BetStatus] = mapped_column(default=BetStatus.UNFINISHED,
                                              server_default=BetStatus.UNFINISHED.value,
                                              nullable=False,
                                              comment='Статус ставки')
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

