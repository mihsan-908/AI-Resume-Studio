from pathlib import Path
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from services.analysis_service import AnalysisService

router = APIRouter(tags=["UI Views"])

templates_path = Path("templates")
templates_path.mkdir(exist_ok=True)
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=RedirectResponse)
def index_redirect():
    return RedirectResponse(url="/dashboard")


@router.get("/dashboard", response_class=HTMLResponse)
def view_dashboard(request: Request, db: Session = Depends(get_db)):
    analyses = AnalysisService.get_all_analyses(db)
    total_analyses = len(analyses)

    avg_ats = round(sum(a.ats_score for a in analyses) / total_analyses, 1) if total_analyses > 0 else 0
    match_scores = [a.job_match_score for a in analyses if a.job_match_score is not None]
    avg_match = round(sum(match_scores) / len(match_scores), 1) if match_scores else None

    latest_analysis = analyses[0] if analyses else None

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "active_page": "dashboard",
            "total_analyses": total_analyses,
            "avg_ats": avg_ats,
            "avg_match": avg_match,
            "latest_analysis": latest_analysis,
            "analyses": analyses[:5]
        }
    )


@router.get("/upload", response_class=HTMLResponse)
def view_upload(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="upload.html",
        context={
            "active_page": "upload"
        }
    )


@router.get("/results/{analysis_id}", response_class=HTMLResponse)
def view_results(analysis_id: int, request: Request, db: Session = Depends(get_db)):
    analysis = AnalysisService.get_analysis_by_id(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis record not found.")

    rewritten = analysis.rewritten_resumes[0] if analysis.rewritten_resumes else None

    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={
            "active_page": "results",
            "analysis": analysis,
            "extracted_resume": analysis.analysis_results.get("extracted_resume", {}),
            "ats_report": analysis.analysis_results.get("ats_report", {}),
            "job_match_report": analysis.analysis_results.get("job_match_report", {}),
            "improvement_report": analysis.analysis_results.get("improvement_report", {}),
            "rewritten_resume": rewritten.rewritten_content if rewritten else {}
        }
    )


@router.get("/resume-builder/{analysis_id}", response_class=HTMLResponse)
def view_resume_builder(analysis_id: int, request: Request, db: Session = Depends(get_db)):
    analysis = AnalysisService.get_analysis_by_id(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis record not found.")

    rewritten_record = analysis.rewritten_resumes[0] if analysis.rewritten_resumes else None

    return templates.TemplateResponse(
        request=request,
        name="resume_builder.html",
        context={
            "active_page": "resume_builder",
            "analysis": analysis,
            "original_resume": analysis.resume,
            "extracted_data": analysis.analysis_results.get("extracted_resume", {}),
            "rewritten_content": rewritten_record.rewritten_content if rewritten_record else {}
        }
    )


@router.get("/history", response_class=HTMLResponse)
def view_history(request: Request, db: Session = Depends(get_db)):
    analyses = AnalysisService.get_all_analyses(db)
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "active_page": "history",
            "analyses": analyses
        }
    )

