from typing import Optional, List, Dict, Any
from fastapi import APIRouter, File, Form, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from services.analysis_service import AnalysisService
from schemas import AnalysisCreateResponse, AnalysisDetailResponse, AnalysisSummary, RewrittenResumeUpdate

router = APIRouter(prefix="/api", tags=["API Endpoints"])


@router.post("/resumes/analyze", response_model=AnalysisCreateResponse)
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Accepts PDF/TXT resume and optional job description, executes the AI Agent pipeline,
    and stores the results in PostgreSQL.
    """
    analysis = AnalysisService.run_full_analysis(db, file, job_description)
    rewritten_record = analysis.rewritten_resumes[0] if analysis.rewritten_resumes else None

    return {
        "status": "success",
        "analysis_id": analysis.id,
        "ats_score": analysis.ats_score,
        "job_match_score": analysis.job_match_score,
        "resume_quality": analysis.resume_quality,
        "projects_count": analysis.projects_count,
        "skills_count": analysis.skills_count,
        "analysis_results": analysis.analysis_results,
        "rewritten_resume": rewritten_record.rewritten_content if rewritten_record else {}
    }


@router.get("/analyses", response_model=List[AnalysisSummary])
def get_analyses(db: Session = Depends(get_db)):
    """Retrieve all historical analyses."""
    analyses = AnalysisService.get_all_analyses(db)
    results = []
    for a in analyses:
        job_title = a.job_description.job_title if a.job_description and a.job_description.job_title else "General Review"
        results.append({
            "id": a.id,
            "resume_filename": a.resume.original_filename if a.resume else "Unknown",
            "job_title": job_title,
            "ats_score": a.ats_score,
            "job_match_score": a.job_match_score,
            "resume_quality": a.resume_quality,
            "projects_count": a.projects_count,
            "skills_count": a.skills_count,
            "created_at": a.created_at
        })
    return results


@router.get("/analyses/{analysis_id}", response_model=AnalysisDetailResponse)
def get_analysis_detail(analysis_id: int, db: Session = Depends(get_db)):
    """Retrieve detailed analysis by ID."""
    analysis = AnalysisService.get_analysis_by_id(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found.")

    rewritten_record = analysis.rewritten_resumes[0] if analysis.rewritten_resumes else None

    return {
        "id": analysis.id,
        "resume_id": analysis.resume_id,
        "job_description_id": analysis.job_description_id,
        "ats_score": analysis.ats_score,
        "job_match_score": analysis.job_match_score,
        "resume_quality": analysis.resume_quality,
        "projects_count": analysis.projects_count,
        "skills_count": analysis.skills_count,
        "analysis_results": analysis.analysis_results,
        "rewritten_resume": rewritten_record.rewritten_content if rewritten_record else {},
        "created_at": analysis.created_at
    }


@router.delete("/analyses/{analysis_id}")
def delete_analysis_endpoint(analysis_id: int, db: Session = Depends(get_db)):
    """Delete an analysis and associated records."""
    success = AnalysisService.delete_analysis(db, analysis_id)
    if not success:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    return {"status": "success", "message": f"Analysis {analysis_id} deleted successfully."}


@router.put("/analyses/{analysis_id}/resume")
def update_resume_sections(analysis_id: int, payload: Dict[str, Any], db: Session = Depends(get_db)):
    """Save user edits to the rewritten resume sections."""
    rewritten_record = AnalysisService.update_rewritten_resume(db, analysis_id, payload)
    return {"status": "success", "version": rewritten_record.version, "rewritten_content": rewritten_record.rewritten_content}
