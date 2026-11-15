# AI Resume Studio - Full-Stack Web Platform

A full-stack, multi-agent AI platform built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, **Jinja2**, and **Chart.js**. It automates resume analysis, ATS compliance scoring, job matching, side-by-side editing, and multi-format document exporting (DOCX, PDF, Markdown, TXT) powered by **Google Gemini**.

---

## 🌟 Key Features

1. **Multi-Agent AI Pipeline**:
   * **ResumeReaderAgent**: Reads and cleans PDF and TXT resumes.
   * **InformationExtractionAgent**: Converts raw resume text into structured JSON.
   * **ATSAgent**: Evaluates ATS compliance, strengths, weaknesses, and calculates a 0–100 ATS score.
   * **JobMatchAgent**: Compares candidate profile against target job description and identifies skill gaps.
   * **ResumeImprovementAgent**: Generates prioritized improvement action items.
   * **ResumeRewriteAgent**: Professional AI rewriting of summary, bullet points, and skills.
   * **ResumeExportAgent**: Coordinates multi-format document exports.

2. **Full-Stack Architecture**:
   * **PostgreSQL & SQLAlchemy**: Persistent relational storage for resumes, job descriptions, analyses, and versioned rewritten resumes.
   * **Alembic**: Database migrations management.
   * **Jinja2 Templates & Modular Assets**: Pure HTML5 templates (`base.html`, `dashboard.html`, `upload.html`, `results.html`, `resume_builder.html`, `history.html`) with separate CSS stylesheets and JavaScript files.
   * **Chart.js Visualizations**: Interactive ATS score gauge, skill category breakdown pie chart, section completeness bar chart, and job match score indicators.
   * **Interactive Side-by-Side Builder**: Compare original resume content against AI-rewritten content in split-screen mode, edit sections directly, save custom revisions, and download exports.
   * **4 Document Export Formats**: Export final user-approved resumes as **DOCX**, **PDF**, **Markdown**, or **TXT**.

---

## 🛠️ Project Structure

```
AI-Resume-Studio/
├── main.py                         # Application entrypoint & FastAPI app initialization
├── database.py                     # PostgreSQL connection engine & session management
├── models.py                       # SQLAlchemy ORM models (Resumes, JobDescriptions, Analyses, etc.)
├── schemas.py                      # Pydantic schemas for request/response validation
├── config.py                       # Model & directory settings
├── alembic.ini / alembic/          # Database migration files
│
├── agents/                         # Core AI Agent classes
├── prompts/                        # LLM System Prompts
├── utils/                          # File readers, clean text utilities, & Exporters (DOCX/PDF/MD/TXT)
├── services/                       # Analysis & Export orchestration service layer
├── routers/                        # API routes & HTML template view routers
│
├── templates/                      # Modular Jinja2 HTML Templates
│   ├── base.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── results.html
│   ├── resume_builder.html
│   └── history.html
│
└── static/                         # Frontend Static Assets
    ├── css/                        # style.css, dashboard.css, upload.css, results.css...
    └── js/                         # main.js, dashboard.js, upload.js, results.js, resume_builder.js...
```

---

## 🚀 Setup & Installation

### 1. Prerequisites
* Python 3.10+
* PostgreSQL database (e.g. `resume_database`)

### 2. Environment Configuration
Create or update `.env` in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql+psycopg2://user:your_password@localhost:5432/resume_database
```

### 3. Install Dependencies
```powershell
.\venv\Scripts\pip.exe install -r requirements.txt
```

### 4. Apply Database Migrations
```powershell
.\venv\Scripts\alembic.exe upgrade head
```

---

## 🏃 Running the Application

To start the FastAPI web server, run:

```powershell
python main.py
```
*(or `uvicorn main:app --reload`)*

Then open your browser and navigate to:
👉 **`http://127.0.0.1:8000`**

---

## 🧪 Running Tests

To run the automated test suite:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_app.py
```

---

## 🔗 REST API Endpoints

* **`POST /api/resumes/analyze`**: Accepts resume PDF file and optional job description text. Returns analysis JSON.
* **`GET /api/analyses`**: Lists historical analysis records.
* **`GET /api/analyses/{id}`**: Gets full analysis details.
* **`DELETE /api/analyses/{id}`**: Deletes analysis record.
* **`PUT /api/analyses/{id}/resume`**: Saves user-edited rewritten resume sections.
* **`GET /api/analyses/{id}/export/{format}`**: Downloads document export (`pdf`, `docx`, `md`, `txt`).
