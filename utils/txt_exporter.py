from pathlib import Path

class TXTExporter:
    """
    Export rewritten resume as a TXT file.
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

                file.write("AI REWRITTEN RESUME\n")
                file.write("=" * 60 + "\n\n")

                file.write("PROFESSIONAL SUMMARY\n\n")

                file.write(
                    report.get(
                        "professional_summary",
                        ""
                    )
                )

                file.write("\n\n")

                file.write("SKILLS\n")

                for category, skills in report.get(
                    "skills",
                    {}
                ).items():

                    file.write(f"\n{category}\n")

                    for skill in skills:

                        file.write(
                            f"  • {skill}\n"
                        )

                file.write("\n")

                file.write("PROJECTS\n")

                for project in report.get(
                    "projects",
                    []
                ):

                    file.write(
                        f"\n{project.get('title')}\n"
                    )

                    for bullet in project.get(
                        "rewritten_description",
                        []
                    ):

                        file.write(
                            f"  • {bullet}\n"
                        )

                file.write("\n")

                file.write("FINAL RESUME TIPS\n")

                for tip in report.get(
                    "final_resume_tips",
                    []
                ):

                    file.write(
                        f"  • {tip}\n"
                    )

            return True

        except Exception as error:

            raise Exception(
                f"TXT export failed: {error}"
            )