import json
from agents.base_agent import BaseAgent

from prompts.resume_rewrite_prompt import (
    RESUME_REWRITE_PROMPT
)

from utils.json_reader import load_json
from utils.json_writer import save_json
from utils.json_parser import parse_json


class ResumeRewriteAgent(BaseAgent):
    """
    AI Agent responsible for rewriting
    resume sections professionally.
    """

    def __init__(self):
        super().__init__()

    def rewrite_resume(
        self,
        resume_path: str,
        ats_path: str,
        job_match_path: str,
        improvement_path: str,
        output_path: str
    ) -> dict:

        self.console.rule(
            "[bold cyan]Resume Rewrite Agent"
        )

        self.console.print(
            "[cyan]Generating improved resume...[/cyan]"
        )

        resume = load_json(
            resume_path
        )

        ats = load_json(
            ats_path
        )

        job_match = load_json(
            job_match_path
        )

        improvements = load_json(
            improvement_path
        )

        prompt = RESUME_REWRITE_PROMPT

        prompt = prompt.replace(
            "<<RESUME>>",
            json.dumps(
                resume,
                indent=4
            )
        )

        prompt = prompt.replace(
            "<<ATS>>",
            json.dumps(
                ats,
                indent=4
            )
        )

        prompt = prompt.replace(
            "<<JOB_MATCH>>",
            json.dumps(
                job_match,
                indent=4
            )
        )

        prompt = prompt.replace(
            "<<IMPROVEMENTS>>",
            json.dumps(
                improvements,
                indent=4
            )
        )

        response = self.llm.generate_response(prompt)

        if not response or not response.strip():
         raise ValueError(
           "LLM returned an empty response."
        )

        rewritten_resume = parse_json(response)

        if not rewritten_resume:
         raise ValueError(
          "Unable to parse rewritten resume JSON."
        )

        required_fields = [
            "professional_summary",
            "skills",
            "projects",
            "experience",
            "final_resume_tips"
        ]

        for field in required_fields:

          if field not in rewritten_resume:

           rewritten_resume[field] = (
                {} if field == "skills"
                else []
            )

        if not rewritten_resume["professional_summary"]:
            rewritten_resume[
                "professional_summary"
                ] = "Professional summary not generated."
            
        save_json(
            rewritten_resume,
            output_path
        )

        self.console.print(
            "[green]✓ Resume rewritten successfully[/green]"
        )

        self.console.print(
            f"[green]✓ Report saved to {output_path}[/green]"
        )

        return rewritten_resume