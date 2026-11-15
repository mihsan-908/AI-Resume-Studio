from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class PDFExporter:
    """
    Export rewritten resume as a clean, professionally formatted PDF file using ReportLab.
    """

    def export(self, report: dict, output_path: str) -> bool:
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=40,
                leftMargin=40,
                topMargin=40,
                bottomMargin=40,
            )

            styles = getSampleStyleSheet()

            # Custom styles
            title_style = ParagraphStyle(
                "DocTitle",
                parent=styles["Heading1"],
                fontName="Helvetica-Bold",
                fontSize=20,
                leading=24,
                textColor=colors.HexColor("#0f172a"),
                spaceAfter=12,
            )

            heading_style = ParagraphStyle(
                "SectionHeading",
                parent=styles["Heading2"],
                fontName="Helvetica-Bold",
                fontSize=14,
                leading=18,
                textColor=colors.HexColor("#0284c7"),
                spaceBefore=12,
                spaceAfter=6,
            )

            subheading_style = ParagraphStyle(
                "SubHeading",
                parent=styles["Heading3"],
                fontName="Helvetica-Bold",
                fontSize=11,
                leading=14,
                textColor=colors.HexColor("#334155"),
                spaceBefore=6,
                spaceAfter=4,
            )

            body_style = ParagraphStyle(
                "BodyTextCustom",
                parent=styles["Normal"],
                fontName="Helvetica",
                fontSize=10,
                leading=14,
                textColor=colors.HexColor("#1e293b"),
                spaceAfter=6,
            )

            bullet_style = ParagraphStyle(
                "BulletCustom",
                parent=body_style,
                leftIndent=15,
                firstLineIndent=-10,
                spaceAfter=3,
            )

            story = []

            # Document Title
            story.append(Paragraph("AI Rewritten Resume", title_style))
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=14))

            # Professional Summary
            summary_text = report.get("professional_summary", "")
            if summary_text:
                story.append(Paragraph("Professional Summary", heading_style))
                story.append(Paragraph(summary_text, body_style))
                story.append(Spacer(1, 8))

            # Skills Section
            skills_dict = report.get("skills", {})
            if skills_dict:
                story.append(Paragraph("Skills & Technical Expertise", heading_style))
                for category, skill_list in skills_dict.items():
                    if skill_list:
                        skills_str = ", ".join(skill_list)
                        story.append(Paragraph(f"<b>{category}:</b> {skills_str}", body_style))
                story.append(Spacer(1, 8))

            # Projects Section
            projects = report.get("projects", [])
            if projects:
                story.append(Paragraph("Key Projects & Accomplishments", heading_style))
                for proj in projects:
                    p_title = proj.get("title", "Project")
                    story.append(Paragraph(p_title, subheading_style))
                    for bullet in proj.get("rewritten_description", []):
                        story.append(Paragraph(f"• {bullet}", bullet_style))
                    story.append(Spacer(1, 4))
                story.append(Spacer(1, 8))

            # Experience Section
            experience = report.get("experience", [])
            if experience:
                story.append(Paragraph("Work Experience", heading_style))
                for exp in experience:
                    comp = exp.get("company", exp.get("role", "Work Experience"))
                    story.append(Paragraph(comp, subheading_style))
                    for bullet in exp.get("rewritten_points", []):
                        story.append(Paragraph(f"• {bullet}", bullet_style))
                    story.append(Spacer(1, 4))
                story.append(Spacer(1, 8))

            # Tips Section
            tips = report.get("final_resume_tips", [])
            if tips:
                story.append(Paragraph("Final Resume Tips", heading_style))
                for tip in tips:
                    story.append(Paragraph(f"✓ {tip}", bullet_style))

            doc.build(story)
            return True

        except Exception as error:
            raise Exception(f"PDF export failed: {error}")
