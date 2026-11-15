import os
from pathlib import Path
from typing import Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import Analysis, RewrittenResume
from utils.docx_exporter import DOCXExporter
from utils.pdf_exporter import PDFExporter
from utils.markdown_exporter import MarkdownExporter
from utils.txt_exporter import TXTExporter
from config import OUTPUT_FOLDER


class ExportService:

    @staticmethod
    def generate_export(db: Session, analysis_id: int, file_format: str) -> Tuple[str, str, str]:
        """
        Generates exported document from the approved rewritten resume content stored in DB.
        Returns: (file_path, media_type, download_filename)
        """
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis record not found.")

        rewritten_record = db.query(RewrittenResume).filter(RewrittenResume.analysis_id == analysis_id).first()
        if not rewritten_record or not rewritten_record.rewritten_content:
            raise HTTPException(status_code=404, detail="Rewritten resume content not found.")

        report = rewritten_record.rewritten_content
        file_format = file_format.lower().strip()

        output_dir = Path(OUTPUT_FOLDER)
        output_dir.mkdir(parents=True, exist_ok=True)

        filename_prefix = f"Analysis_{analysis_id}_Rewritten_Resume"

        if file_format == "docx":
            file_path = output_dir / f"{filename_prefix}.docx"
            exporter = DOCXExporter()
            exporter.export(report, str(file_path))
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            download_name = f"Rewritten_Resume_{analysis_id}.docx"

        elif file_format == "pdf":
            file_path = output_dir / f"{filename_prefix}.pdf"
            exporter = PDFExporter()
            exporter.export(report, str(file_path))
            media_type = "application/pdf"
            download_name = f"Rewritten_Resume_{analysis_id}.pdf"

        elif file_format == "md":
            file_path = output_dir / f"{filename_prefix}.md"
            exporter = MarkdownExporter()
            exporter.export(report, str(file_path))
            media_type = "text/markdown"
            download_name = f"Rewritten_Resume_{analysis_id}.md"

        elif file_format == "txt":
            file_path = output_dir / f"{filename_prefix}.txt"
            exporter = TXTExporter()
            exporter.export(report, str(file_path))
            media_type = "text/plain"
            download_name = f"Rewritten_Resume_{analysis_id}.txt"

        else:
            raise HTTPException(status_code=400, detail="Invalid export format. Supported: pdf, docx, md, txt.")

        return str(file_path), media_type, download_name
