from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class JobDescriptionBase(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    description_text: str


class ResumeBase(BaseModel):
    original_filename: str
    extracted_text: str


class RewrittenResumeUpdate(BaseModel):
    professional_summary: Optional[str] = None
    skills: Optional[Dict[str, List[str]]] = None
    projects: Optional[List[Dict[str, Any]]] = None
    experience: Optional[List[Dict[str, Any]]] = None
    final_resume_tips: Optional[List[str]] = None


class AnalysisSummary(BaseModel):
    id: int
    resume_filename: str
    job_title: Optional[str] = "General Review"
    ats_score: float
    job_match_score: Optional[float] = None
    resume_quality: str
    projects_count: int
    skills_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnalysisDetailResponse(BaseModel):
    id: int
    resume_id: int
    job_description_id: Optional[int] = None
    ats_score: float
    job_match_score: Optional[float] = None
    resume_quality: str
    projects_count: int
    skills_count: int
    analysis_results: Dict[str, Any]
    rewritten_resume: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnalysisCreateResponse(BaseModel):
    status: str
    analysis_id: int
    ats_score: float
    job_match_score: Optional[float] = None
    resume_quality: str
    projects_count: int
    skills_count: int
    analysis_results: Dict[str, Any]
    rewritten_resume: Dict[str, Any]
