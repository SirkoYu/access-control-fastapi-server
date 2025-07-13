from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func


class TimestampMixin():
    timestamp: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), 
        server_default=func.now(),
    )