"""Shared environment configuration for the pipeline command-line runners."""
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent


def load_env():
    """Load only the project-root .env, preserving existing environment variables."""
    load_dotenv(ROOT / ".env", override=False)
