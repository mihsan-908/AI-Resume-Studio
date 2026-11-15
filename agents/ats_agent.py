import json
from agents.base_agent import BaseAgent
from prompts.ats_prompt import ATS_PROMPT
from utils.json_reader import load_json
from utils.json_parser import parse_json
from utils.json_writer import save_json


class ATSAgent(BaseAgent):
    """
    AI Agent responsible for evaluating
    ATS compatibility.
    """

    def __init__(self):
        super().__init__()

    def evaluate_resume(self, resume_json_path: str, output_path: str) -> dict:

        self.console.rule("[bold magenta]ATS Evaluation Agent")

        self.console.print(
            "[cyan]Evaluating ATS compatibility...[/cyan]"
        )

        resume_data = load_json(resume_json_path)

        prompt = ATS_PROMPT.replace(
            "<<RESUME_DATA>>",
            json.dumps(resume_data, indent=4)
        )

        response = self.llm.generate_response(prompt)

        ats_report = parse_json(response)

        save_json(
            ats_report,
            output_path
        )

        self.console.print(
            "[green]✓ ATS evaluation completed[/green]"
        )

        self.console.print(
            f"[green]✓ Report saved to {output_path}[/green]"
        )

        return ats_report