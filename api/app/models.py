# app/models.py

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Log(Base):
    __tablename__ = 'logs'

    userid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chatid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    llm_model_name = Column(String, nullable=False, default='zephyr')
    timestamp = Column(DateTime, default=datetime.utcnow)
    pdf_file_name = Column(String, nullable=False)
    pdf_file_id = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    pdf_upload_time = Column(DateTime, default=datetime.utcnow)
    uploaded_by = Column(UUID(as_uuid=True), nullable=False)
