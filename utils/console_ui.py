from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

def get_job_description() -> str:
    """
    Read job description either from terminal
    or from a text file.
    """

    console.rule("[bold yellow]Job Description")

    console.print("[1] Paste Job Description")
    console.print("[2] Load from Text File\n")

    choice = input(
        "Choose an option (1/2): "
    ).strip()

    if choice == "2":

        file_name = input(
            "\nEnter TXT file name: "
        ).strip()

        job_folder = Path(
            "uploads/job_descriptions"
        )

        path = job_folder / file_name

        if not path.exists():
            raise FileNotFoundError(
                "Job description file not found."
            )

        return path.read_text(
            encoding="utf-8"
        )

    console.print(
        "\nPaste the Job Description."
    )

    console.print(
        "Press Enter twice to finish.\n"
    )

    lines = []

    while True:

        line = input()

        if line == "":
            break

        lines.append(line)

    return "\n".join(lines)

def display_ats_report(report: dict):

    console.rule("[bold magenta]ATS Evaluation Report")

    console.print(
        f"[bold cyan]ATS Score:[/bold cyan] {report.get('ats_score',0)}/100\n"
    )

    table = Table(
        show_header=True,
        header_style="bold blue"
    )

    table.add_column(
        "Category",
        width=28
    )

    table.add_column(
        "Details"
    )

    table.add_row(
        "Overall Verdict",
        report.get(
            "overall_verdict",
            ""
        )
    )

    table.add_row(
        "Strengths",
        "\n".join(
            report.get(
                "strengths",
                []
            )
        )
    )

    table.add_row(
        "Weaknesses",
        "\n".join(
            report.get(
                "weaknesses",
                []
            )
        )
    )

    table.add_row(
        "Missing Sections",
        "\n".join(
            report.get(
                "missing_sections",
                []
            )
        )
    )

    table.add_row(
        "Keyword Suggestions",
        "\n".join(
            report.get(
                "keyword_suggestions",
                []
            )
        )
    )

    table.add_row(
        "Formatting Suggestions",
        "\n".join(
            report.get(
                "formatting_suggestions",
                []
            )
        )
    )

    console.print(table)

def display_job_match_report(report: dict):

    console.rule("[bold yellow]Job Match Report")

    console.print(
        f"[bold cyan]Match Score:[/bold cyan] {report.get('match_score',0)}/100\n"
    )

    table = Table(
        show_header=True,
        header_style="bold blue"
    )

    table.add_column(
        "Category",
        width=28
    )

    table.add_column(
        "Details"
    )

    table.add_row(
        "Overall Match",
        report.get(
            "overall_match",
            ""
        )
    )

    table.add_row(
        "Matching Skills",
        "\n".join(
            report.get(
                "matching_skills",
                []
            )
        )
    )

    table.add_row(
        "Missing Skills",
        "\n".join(
            report.get(
                "missing_skills",
                []
            )
        )
    )

    table.add_row(
        "Matching Qualifications",
        "\n".join(
            report.get(
                "matching_qualifications",
                []
            )
        )
    )

    table.add_row(
        "Missing Qualifications",
        "\n".join(
            report.get(
                "missing_qualifications",
                []
            )
        )
    )

    table.add_row(
        "Recommendations",
        "\n".join(
            report.get(
                "recommendations",
                []
            )
        )
    )

    console.print(table)

def display_resume_improvements(report: dict):

    console.rule(
        "[bold green]Resume Improvement Report"
    )

    table = Table(
        show_header=True,
        header_style="bold blue"
    )

    table.add_column(
        "Category",
        width=30
    )

    table.add_column(
        "Details"
    )

    table.add_row(
        "Summary",
        report.get(
            "summary",
            ""
        )
    )

    table.add_row(
        "High Priority",
        "\n".join(
            report.get(
                "high_priority_improvements",
                []
            )
        )
    )

    table.add_row(
        "Medium Priority",
        "\n".join(
            report.get(
                "medium_priority_improvements",
                []
            )
        )
    )

    table.add_row(
        "Low Priority",
        "\n".join(
            report.get(
                "low_priority_improvements",
                []
            )
        )
    )

    table.add_row(
        "Recommended Skills",
        "\n".join(
            report.get(
                "recommended_skills",
                []
            )
        )
    )

    table.add_row(
        "Recommended Certifications",
        "\n".join(
            report.get(
                "recommended_certifications",
                []
            )
        )
    )

    table.add_row(
        "Recommended Projects",
        "\n".join(
            report.get(
                "recommended_projects",
                []
            )
        )
    )

    table.add_row(
        "Final Advice",
        report.get(
            "final_advice",
            ""
        )
    )

    console.print(table)

def display_rewritten_resume(report: dict):

    console.rule(
        "[bold cyan]AI Rewritten Resume"
    )

    console.print(
        "[bold yellow]Professional Summary[/bold yellow]\n"
    )

    console.print(
        report.get(
            "professional_summary",
            "Not Available"
        )
    )

    console.print()

    skill_table = Table(
        title="Skills",
        show_header=True,
        header_style="bold blue"
    )

    skill_table.add_column(
        "Category",
        width=30
    )

    skill_table.add_column(
        "Skills"
    )

    for category, skills in report.get(
        "skills",
        {}
    ).items():

        skill_table.add_row(
            category,
            ", ".join(skills)
        )

    console.print(skill_table)

    console.print()

    console.print(
        "[bold yellow]Projects[/bold yellow]"
    )

    for project in report.get(
        "projects",
        []
    ):
        console.print()

        console.print(
            f"[bold green]{project.get('title')}[/bold green]"
        )

        console.print()

        for bullet in project.get(
            "rewritten_description",
            []
        ):
            console.print(
                f"[green]•[/green] {bullet}"
            )

        console.print()

    experience = report.get(
        "experience",
        []
    )

    if experience:

        console.print()

        console.print(
            "[bold yellow]Experience[/bold yellow]"
        )

        for job in experience:

            console.print(
                f"\n[bold green]{job.get('company')}[/bold green]"
            )

            for bullet in job.get(
                "rewritten_points",
                []
            ):
                console.print(
                    f" • {bullet}"
                )

    console.print()

    console.rule(
        "[bold yellow]Final Resume Tips"
    )

    for tip in report.get(
        "final_resume_tips",
        []
    ):

        console.print(
            f"[cyan]✓[/cyan] {tip}"
        )

def display_pipeline_summary(
    ats_report: dict,
    job_match_report: dict,
    extracted_resume_path: str,
    ats_report_path: str,
    job_match_path: str,
    improvement_path: str,
    rewritten_resume_path: str
):
    """
    Display final pipeline summary.
    """

    console.rule(
        "[bold green]Pipeline Summary"
    )

    table = Table(
        show_header=True,
        header_style="bold green"
    )

    table.add_column(
        "Step",
        width=35
    )

    table.add_column(
        "Status"
    )

    table.add_row(
        "Resume Processed",
         "[green]✔ Completed[/green]"
    )

    table.add_row(
        "Information Extracted",
        "[green]✔ Completed[/green]"
    )

    table.add_row(
        "ATS Evaluation",
        f"[cyan]{ats_report.get('ats_score',0)}/100[/cyan]"
    )

    table.add_row(
        "Job Match Analysis",
        f"[cyan]{job_match_report.get('match_score',0)}/100[/cyan]"
    )

    table.add_row(
        "Resume Improvements",
        "[green]✔ Generated[/green]"
    )

    table.add_row(
        "Resume Rewrite",
        "[green]✔ Generated[/green]"
    )

    table.add_row(
        "Resume Export",
        "[green]✔ Completed[/green]"
    )

    console.print(table)

    console.print()

    console.rule(
        "[bold cyan]Generated Reports"
    )

    report_table = Table(
        show_header=True,
        header_style="bold cyan"
    )

    report_table.add_column(
        "Report",
        width=30
    )

    report_table.add_column(
        "Location"
    )

    report_table.add_row(
        "Extracted Resume",
        extracted_resume_path
    )

    report_table.add_row(
        "ATS Report",
        ats_report_path
    )

    report_table.add_row(
        "Job Match Report",
        job_match_path
    )

    report_table.add_row(
        "Improvement Report",
        improvement_path
   )

    report_table.add_row(
        "Rewritten Resume",
        rewritten_resume_path
    )

    console.print(
        report_table
    )

    console.print()

    console.rule(
        "[bold cyan]Exported Resume Files"
    )

    export_table = Table(
        show_header=True,
        header_style="bold cyan"
    )

    export_table.add_column(
        "Format",
        width=20
    )

    export_table.add_column(
        "Location"
    )

    export_table.add_row(
        "TXT",
        "output/rewritten_resume.txt"
    )

    export_table.add_row(
        "Markdown",
        "output/rewritten_resume.md"
    )

    export_table.add_row(
        "DOCX",
        "output/rewritten_resume.docx"
    )

    console.print(export_table)

    console.rule(
    "[bold green]Analysis Completed Successfully"
    )

    console.print()

    console.print(
        "[bold cyan]Thank you for using Resume Analyzer AI Agent[/bold cyan]"
    )

    console.print()

    console.print(
        "[green]All reports have been generated successfully.[/green]"
    )