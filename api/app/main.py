# app/main.py

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, get_session
from app.models import Base, Log
from sqlalchemy.future import select
import uuid

app = FastAPI()

# Event handler to create tables at startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Endpoint to initialize data
@app.post("/initialize_data")
async def initialize_data(session: AsyncSession = Depends(get_session)):
    new_log = Log(
        pdf_file_name="example_document.pdf",
        uploaded_by=uuid.uuid4()  # Simulating a user ID
    )
    session.add(new_log)
    await session.commit()
    await session.refresh(new_log)
    return {"message": "Data initialized", "log": {
        "userid": str(new_log.userid),
        "chatid": str(new_log.chatid),
        "llm_model_name": new_log.llm_model_name,
        "timestamp": new_log.timestamp,
        "pdf_file_name": new_log.pdf_file_name,
        "pdf_file_id": str(new_log.pdf_file_id),
        "pdf_upload_time": new_log.pdf_upload_time,
        "uploaded_by": str(new_log.uploaded_by),
    }}

# Endpoint to retrieve logs
@app.get("/logs")
async def get_logs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Log))
    logs = result.scalars().all()
    return [
        {
            "userid": str(log.userid),
            "chatid": str(log.chatid),
            "llm_model_name": log.llm_model_name,
            "timestamp": log.timestamp,
            "pdf_file_name": log.pdf_file_name,
            "pdf_file_id": str(log.pdf_file_id),
            "pdf_upload_time": log.pdf_upload_time,
            "uploaded_by": str(log.uploaded_by),
        }
        for log in logs
    ]
