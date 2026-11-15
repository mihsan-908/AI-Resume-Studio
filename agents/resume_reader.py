from agents.base_agent import BaseAgent
from utils.file_handler import extract_resume_text
from utils.text_cleaner import clean_resume_text


class ResumeReaderAgent(BaseAgent):
    """
    Agent responsible for reading resume files.
    """

    def __init__(self):
        super().__init__()

    def process(self, file_path: str) -> str:

        self.console.rule("[bold blue]Resume Reader Agent")

        self.console.print("[cyan]Reading resume...[/cyan]")

        resume_text = extract_resume_text(file_path)
        resume_text = clean_resume_text(resume_text)    

        if not resume_text.strip():
            raise ValueError("Uploaded resume is empty.")

        self.console.print("[green]✓ Resume loaded successfully[/green]")

        self.console.print(
            f"[cyan]Characters:[/cyan] {len(resume_text)}"
        )

        return resume_text