import sys
from rich.console import Console
from utils.gemini_client import GeminiClient

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class BaseAgent:
    """
    Base class for all AI agents.
    """

    def __init__(self):

        self.console = Console()

        self.llm = GeminiClient()