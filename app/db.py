from sqlalchemy import create_engine, String, Integer, DateTime, Text, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///dulce_maitena.db", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)


class Base(DeclarativeBase):
    pass


class ConversationState(Base):
    __tablename__ = "conversation_states"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel: Mapped[str] = mapped_column(String(20))
    user_id: Mapped[str] = mapped_column(String(100), index=True)
    state: Mapped[str] = mapped_column(String(50), default="new")
    notes: Mapped[str] = mapped_column(Text, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MessageLog(Base):
    __tablename__ = "message_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel: Mapped[str] = mapped_column(String(20), index=True)
    user_id: Mapped[str] = mapped_column(String(100), index=True)
    role: Mapped[str] = mapped_column(String(20))
    message_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)



def init_db() -> None:
    Base.metadata.create_all(bind=engine)



def log_message(channel: str, user_id: str, role: str, message_text: str) -> None:
    with SessionLocal() as session:
        session.add(MessageLog(channel=channel, user_id=user_id, role=role, message_text=message_text))
        session.commit()



def get_recent_messages(channel: str, user_id: str, limit: int = 10) -> list[dict]:
    with SessionLocal() as session:
        stmt = (
            select(MessageLog)
            .where(MessageLog.channel == channel, MessageLog.user_id == user_id)
            .order_by(MessageLog.created_at.desc())
            .limit(limit)
        )
        rows = list(session.scalars(stmt))
        rows.reverse()
        return [{"role": row.role, "content": row.message_text} for row in rows]



def upsert_state(channel: str, user_id: str, state: str, notes: str = "") -> None:
    with SessionLocal() as session:
        stmt = select(ConversationState).where(
            ConversationState.channel == channel,
            ConversationState.user_id == user_id,
        )
        row = session.scalars(stmt).first()
        if row is None:
            row = ConversationState(channel=channel, user_id=user_id, state=state, notes=notes)
            session.add(row)
        else:
            row.state = state
            row.notes = notes
            row.updated_at = datetime.utcnow()
        session.commit()



def get_state(channel: str, user_id: str) -> ConversationState | None:
    with SessionLocal() as session:
        stmt = select(ConversationState).where(
            ConversationState.channel == channel,
            ConversationState.user_id == user_id,
        )
        return session.scalars(stmt).first()
