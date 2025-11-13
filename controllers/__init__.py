"""Controllers package for MindlyAI endpoints.

Each module exposes a `register(app, ...)` function that main.py calls to
attach routes to the FastAPI application. This avoids circular imports and
keeps endpoint logic modular.
"""

__all__ = ["health", "detect", "speak", "analyze"]
