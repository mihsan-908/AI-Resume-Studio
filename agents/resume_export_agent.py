from rich.console import Console
from utils.json_handler import load_json
from utils.txt_exporter import TXTExporter
from utils.markdown_exporter import MarkdownExporter
from utils.docx_exporter import DOCXExporter


class ResumeExportAgent:

    def __init__(self):

        self.console = Console()

        self.txt_exporter = TXTExporter()
        self.md_exporter = MarkdownExporter()
        self.docx_exporter = DOCXExporter()

    def export_resume(
        self,
        rewritten_resume_path: str,
        txt_output_path: str,
        md_output_path: str,
        docx_output_path: str
    ) -> dict:

        self.console.rule(
            "[bold cyan]Resume Export Agent"
        )

        self.console.print(
            "Exporting rewritten resume..."
        )

        report = load_json(
            rewritten_resume_path
        )

        self.txt_exporter.export(
            report,
            txt_output_path
        )

        self.md_exporter.export(
            report,
            md_output_path
        )

        self.docx_exporter.export(
            report,
            docx_output_path
        )

        exported_files = {
            "TXT": txt_output_path,
            "Markdown": md_output_path,
            "DOCX": docx_output_path
        }

        self.console.print()

        self.console.print(
            "[bold green]Generated Files[/bold green]"
        )

        for file_type, path in exported_files.items():

            self.console.print(
                f"[green]✓[/green] {file_type:<10} {path}"
            )

            self.console.print()

            self.console.print(
                "[bold green]✓ Export completed successfully[/bold green]"
            )

            return exported_files