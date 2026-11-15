from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import get_db
from services.export_service import ExportService

router = APIRouter(prefix="/api", tags=["Downloads & Exports"])


@router.get("/analyses/{analysis_id}/export/{format}")
def download_resume_format(analysis_id: int, format: str, db: Session = Depends(get_db)):
    """
    Downloads exported resume in PDF, DOCX, MD, or TXT format from approved DB content.
    """
    file_path, media_type, download_name = ExportService.generate_export(db, analysis_id, format)

    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=download_name
    )
