import shutil
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from models import Resume, JobDescription, Analysis, RewrittenResume
from agents.resume_reader import ResumeReaderAgent
from agents.information_extractor import InformationExtractionAgent
from agents.ats_agent import ATSAgent
from agents.job_match_agent import JobMatchAgent
from agents.improvement_agent import ResumeImprovementAgent
from agents.resume_rewrite_agent import ResumeRewriteAgent
from agents.resume_export_agent import ResumeExportAgent

from config import (
    UPLOAD_FOLDER,
    EXTRACTED_RESUME_JSON,
    ATS_REPORT_JSON,
    JOB_MATCH_REPORT_JSON,
    RESUME_IMPROVEMENTS_JSON,
    REWRITTEN_RESUME_JSON,
    REWRITTEN_RESUME_TXT,
    REWRITTEN_RESUME_MD,
    REWRITTEN_RESUME_DOCX,
)


class AnalysisService:

    @staticmethod
    def run_full_analysis(
        db: Session,
        file: UploadFile,
        job_description_text: Optional[str] = None
    ) -> Analysis:
        """
        Executes the AI Agent pipeline and persists the resume, job description,
        analysis scores, and rewritten output into the database.
        """
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file selected.")

        # Sanitize filename against directory traversal
        clean_filename = Path(file.filename).name
        file_ext = Path(clean_filename).suffix.lower()
        if file_ext not in [".pdf", ".txt"]:
            raise HTTPException(
                status_code=400, detail="Unsupported file format. Please upload a PDF or TXT file."
            )

        # Enforce maximum upload size (15 MB limit)
        max_file_size = 15 * 1024 * 1024
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        if file_size > max_file_size:
            raise HTTPException(
                status_code=400, detail="File too large. Maximum supported upload size is 15MB."
            )

        # Save resume file locally with a unique prefix to prevent collisions
        resumes_dir = Path(UPLOAD_FOLDER) / "resumes"
        resumes_dir.mkdir(parents=True, exist_ok=True)
        unique_filename = f"{uuid.uuid4().hex[:8]}_{clean_filename}"
        saved_file_path = resumes_dir / unique_filename

        try:
            with open(saved_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

        try:
            # 1. Read & Clean
            reader = ResumeReaderAgent()
            resume_text = reader.process(str(saved_file_path))

            # 2. Extract Information
            extractor = InformationExtractionAgent()
            extracted_data = extractor.extract_information(resume_text)

            # 3. ATS Evaluation
            ats_agent = ATSAgent()
            ats_report = ats_agent.evaluate_resume(EXTRACTED_RESUME_JSON, ATS_REPORT_JSON)

            # 4. Job Match Evaluation
            job_match_report = {}
            job_desc_obj = None
            if job_description_text and job_description_text.strip():
                job_match_agent = JobMatchAgent()
                job_match_report = job_match_agent.match_resume(
                    EXTRACTED_RESUME_JSON,
                    job_description_text.strip(),
                    JOB_MATCH_REPORT_JSON
                )
                job_desc_obj = JobDescription(
                    description_text=job_description_text.strip()
                )
                db.add(job_desc_obj)
                db.flush()

            # 5. Improvement Suggestions
            improvement_agent = ResumeImprovementAgent()
            improvement_report = improvement_agent.generate_improvements(
                EXTRACTED_RESUME_JSON,
                ATS_REPORT_JSON,
                JOB_MATCH_REPORT_JSON if job_match_report else ATS_REPORT_JSON,
                RESUME_IMPROVEMENTS_JSON
            )

            # 6. Resume Rewrite
            rewrite_agent = ResumeRewriteAgent()
            rewritten_resume = rewrite_agent.rewrite_resume(
                EXTRACTED_RESUME_JSON,
                ATS_REPORT_JSON,
                JOB_MATCH_REPORT_JSON if job_match_report else ATS_REPORT_JSON,
                RESUME_IMPROVEMENTS_JSON,
                REWRITTEN_RESUME_JSON
            )

            # 7. Initial Formats Export
            export_agent = ResumeExportAgent()
            export_agent.export_resume(
                REWRITTEN_RESUME_JSON,
                REWRITTEN_RESUME_TXT,
                REWRITTEN_RESUME_MD,
                REWRITTEN_RESUME_DOCX
            )

            # Count metrics
            ats_score = float(ats_report.get("ats_score", 0))
            match_score = float(job_match_report.get("match_score", 0)) if job_match_report else None

            skills_list = extracted_data.get("skills", [])
            skills_count = len(skills_list) if isinstance(skills_list, list) else 0

            projects_list = extracted_data.get("projects", [])
            projects_count = len(projects_list) if isinstance(projects_list, list) else 0

            if ats_score >= 80:
                resume_quality = "Excellent"
            elif ats_score >= 60:
                resume_quality = "Good"
            elif ats_score >= 40:
                resume_quality = "Needs Improvement"
            else:
                resume_quality = "Critical Gaps"

            # Create Resume record
            resume_obj = Resume(
                original_filename=clean_filename,
                extracted_text=resume_text,
                file_path=str(saved_file_path)
            )
            db.add(resume_obj)
            db.flush()

            # Create Analysis record
            combined_results = {
                "extracted_resume": extracted_data,
                "ats_report": ats_report,
                "job_match_report": job_match_report,
                "improvement_report": improvement_report,
            }

            analysis_obj = Analysis(
                resume_id=resume_obj.id,
                job_description_id=job_desc_obj.id if job_desc_obj else None,
                ats_score=ats_score,
                job_match_score=match_score,
                resume_quality=resume_quality,
                projects_count=projects_count,
                skills_count=skills_count,
                analysis_results=combined_results,
            )
            db.add(analysis_obj)
            db.flush()

            # Create RewrittenResume record
            rewritten_obj = RewrittenResume(
                analysis_id=analysis_obj.id,
                rewritten_content=rewritten_resume,
                version=1
            )
            db.add(rewritten_obj)

            db.commit()
            db.refresh(analysis_obj)
            return analysis_obj

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Analysis pipeline error: {str(e)}")

    @staticmethod
    def get_analysis_by_id(db: Session, analysis_id: int) -> Optional[Analysis]:
        return db.query(Analysis).filter(Analysis.id == analysis_id).first()

    @staticmethod
    def get_all_analyses(db: Session) -> List[Analysis]:
        return db.query(Analysis).order_by(Analysis.created_at.desc()).all()

    @staticmethod
    def delete_analysis(db: Session, analysis_id: int) -> bool:
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            return False
        db.delete(analysis)
        db.commit()
        return True

    @staticmethod
    def update_rewritten_resume(db: Session, analysis_id: int, updated_content: Dict[str, Any]) -> RewrittenResume:
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found.")

        rewritten = db.query(RewrittenResume).filter(RewrittenResume.analysis_id == analysis_id).first()
        if not rewritten:
            rewritten = RewrittenResume(analysis_id=analysis_id, rewritten_content=updated_content, version=1)
            db.add(rewritten)
        else:
            rewritten.rewritten_content = updated_content
            rewritten.version += 1

        db.commit()
        db.refresh(rewritten)
        return rewritten
