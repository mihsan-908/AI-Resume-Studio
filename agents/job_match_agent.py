import json
from agents.base_agent import BaseAgent
from prompts.job_match_prompt import JOB_MATCH_PROMPT
from utils.json_reader import load_json
from utils.json_writer import save_json
from utils.json_parser import parse_json


class JobMatchAgent(BaseAgent):
    """
    AI Agent responsible for comparing
    resumes with job descriptions.
    """

    def __init__(self):
        super().__init__()

    def match_resume(
        self,
        resume_json_path: str,
        job_description: str,
        output_path: str
    ) -> dict:

        self.console.rule(
            "[bold yellow]Job Match Agent"
        )

        self.console.print(
            "[cyan]Comparing resume with job description...[/cyan]"
        )

        resume_data = load_json(
            resume_json_path
        )

        prompt = JOB_MATCH_PROMPT.replace(
            "<<RESUME_DATA>>",
            json.dumps(
                resume_data,
                indent=4
            )
        )

        prompt = prompt.replace(
            "<<JOB_DESCRIPTION>>",
            job_description
        )

        response = self.llm.generate_response(
            prompt
        )

        report = parse_json(response)

        save_json(
            report,
            output_path
        )

        self.console.print(
            "[green]✓ Job match completed[/green]"
        )

        self.console.print(
            f"[green]✓ Report saved to {output_path}[/green]"
        )

        return report