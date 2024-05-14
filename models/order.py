import json

from sqlalchemy import (BigInteger, Column, String, select, Date, DateTime,
                        func, Integer, ForeignKey, Boolean, Text, )
from sqlalchemy.orm import relationship
from models.db import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        BigInteger,
        ForeignKey('users.id', ondelete='CASCADE')
    )
    created_at = Column(
        DateTime,
        server_default=func.now()
    )
    qna = Column(Text)

    def set_setting(self, key, value):
        current_settings = json.loads(self.qna) if self.qna else {}
        current_settings[key] = value
        self.qna = json.dumps(current_settings)

    def get_setting(self, key):
        settings = json.loads(self.qna) if self.qna else {}
        return settings.get(key)