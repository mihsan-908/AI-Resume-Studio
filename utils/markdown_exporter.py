from pathlib import Path

class MarkdownExporter:
    """
    Export rewritten resume as Markdown.
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

            with open(
                output_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write("# AI Rewritten Resume\n\n")

                file.write(
                    "## Professional Summary\n\n"
                )

                file.write(
                    report.get(
                        "professional_summary",
                        ""
                    )
                )

                file.write("\n\n")

                file.write("## Skills\n\n")

                for category, skills in report.get(
                    "skills",
                    {}
                ).items():

                    file.write(
                        f"### {category}\n"
                    )

                    for skill in skills:

                        file.write(
                            f"- {skill}\n"
                        )

                    file.write("\n")

                file.write("## Projects\n\n")

                for project in report.get(
                    "projects",
                    []
                ):

                    file.write(
                        f"### {project.get('title')}\n"
                    )

                    for bullet in project.get(
                        "rewritten_description",
                        []
                    ):

                        file.write(
                            f"- {bullet}\n"
                        )

                    file.write("\n")

                file.write(
                    "## Final Resume Tips\n\n"
                )

                for tip in report.get(
                    "final_resume_tips",
                    []
                ):

                    file.write(
                        f"- {tip}\n"
                    )

            return True

        except Exception as error:

            raise Exception(
                f"Markdown export failed: {error}"
            )