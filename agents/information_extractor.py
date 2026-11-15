from agents.base_agent import BaseAgent
from prompts.extraction_prompt import EXTRACTION_PROMPT
from utils.json_parser import parse_json
from utils.json_writer import save_json
from config import EXTRACTED_RESUME_JSON


class InformationExtractionAgent(BaseAgent):
    """
    AI Agent responsible for extracting structured
    information from a resume.
    """

    def __init__(self):
        super().__init__()

    def extract_information(self, resume_text: str) -> dict:

        self.console.rule(
            "[bold green]Information Extraction Agent"
        )

        self.console.print(
            "[cyan]Extracting structured information...[/cyan]"
        )

        prompt = EXTRACTION_PROMPT.replace(
            "<<RESUME_TEXT>>",
            resume_text
        )

        response = self.llm.generate_response(prompt)

        resume_data = parse_json(response)

        save_json(
            resume_data,
            EXTRACTED_RESUME_JSON
        )

        self.console.print(
            "[green]✓ Information extracted successfully[/green]"
        )

        self.console.print(
            f"[green]✓ JSON saved to {EXTRACTED_RESUME_JSON}[/green]"
        )

        return resume_data