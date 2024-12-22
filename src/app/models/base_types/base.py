import datetime
from typing import Annotated
from sqlalchemy.orm import mapped_column
from sqlalchemy import func
from sqlalchemy import (
    BIGINT,
    ForeignKey,
    Integer
)

id_pk = Annotated[int, mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True,
                                    comment='Уникальный идентификатор')]
created_at = Annotated[
    datetime.datetime, mapped_column(nullable=False, comment='Дата создания', server_default=func.now())]
updated_at = Annotated[datetime.datetime, mapped_column(nullable=True, comment='Дата обновления ')]
