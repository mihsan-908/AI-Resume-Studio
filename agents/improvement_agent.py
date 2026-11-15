import json
from agents.base_agent import BaseAgent
from prompts.improvement_prompt import IMPROVEMENT_PROMPT
from utils.json_reader import load_json
from utils.json_writer import save_json
from utils.json_parser import parse_json


class ResumeImprovementAgent(BaseAgent):
    """
    AI Agent responsible for generating
    personalized resume improvement suggestions.
    """

    def __init__(self):
        super().__init__()

    def generate_improvements(
        self,
        resume_path: str,
        ats_path: str,
        job_match_path: str,
        output_path: str
    ) -> dict:

        self.console.rule(
            "[bold green]Resume Improvement Agent"
        )

        self.console.print(
            "[cyan]Generating improvement suggestions...[/cyan]"
        )

        resume = load_json(resume_path)

        ats = load_json(ats_path)

        job_match = load_json(job_match_path)

        prompt = IMPROVEMENT_PROMPT

        prompt = prompt.replace(
            "<<RESUME>>",
            json.dumps(resume, indent=4)
        )

        prompt = prompt.replace(
            "<<ATS>>",
            json.dumps(ats, indent=4)
        )

        prompt = prompt.replace(
            "<<JOB_MATCH>>",
            json.dumps(job_match, indent=4)
        )

        response = self.llm.generate_response(
            prompt
        )

        improvements = parse_json(
            response
        )

        save_json(
            improvements,
            output_path
        )

        self.console.print(
            "[green]✓ Resume improvements generated[/green]"
        )

        self.console.print(
            f"[green]✓ Report saved to {output_path}[/green]"
        )

        return improvements