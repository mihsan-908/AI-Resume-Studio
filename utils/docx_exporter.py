from pathlib import Path
from docx import Document


class DOCXExporter:
    """
    Export rewritten resume as a DOCX file.
    """

    def export(
        self,
        report: dict,
        output_path: str
    ) -> bool:

        try:

            Path(output_path).parent.mkdir(
                parents=True,
                exist_ok=True
            )

            document = Document()

            document.add_heading(
                "AI Rewritten Resume",
                level=1
            )

            document.add_heading(
                "Professional Summary",
                level=2
            )

            document.add_paragraph(
                report.get(
                    "professional_summary",
                    ""
                )
            )

            document.add_heading(
                "Skills",
                level=2
            )

            for category, skills in report.get(
                "skills",
                {}
            ).items():

                document.add_heading(
                    category,
                    level=3
                )

                for skill in skills:

                    document.add_paragraph(
                        skill,
                        style="List Bullet"
                    )

            document.add_heading(
                "Projects",
                level=2
            )

            for project in report.get(
                "projects",
                []
            ):

                document.add_heading(
                    project.get(
                        "title"
                    ),
                    level=3
                )

                for bullet in project.get(
                    "rewritten_description",
                    []
                ):

                    document.add_paragraph(
                        bullet,
                        style="List Bullet"
                    )

            document.add_heading(
                "Final Resume Tips",
                level=2
            )

            for tip in report.get(
                "final_resume_tips",
                []
            ):

                document.add_paragraph(
                    tip,
                    style="List Bullet"
                )

            document.save(
                output_path
            )

            return True

        except Exception as error:

            raise Exception(
                f"DOCX export failed: {error}"
            )