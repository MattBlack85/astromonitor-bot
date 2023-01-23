from sqlalchemy import BINARY, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, mapped_column, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    api_token = Column(String, nullable=False)
    backup = relationship(
        "Backup", uselist=False, back_populates="user", cascade="all, delete", passive_deletes=True, lazy="selectin"
    )


class Backup(Base):
    __tablename__ = "backups"
    id = Column(Integer, primary_key=True)
    content = Column(BINARY, nullable=False)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="backup")
