from fastapi import FastAPI, Query
import os
import time
import socket
import platform
import sys


# Record module import time as a simple uptime baseline (starts when app imports controllers)
START_TIME = time.time()


def register(app: FastAPI):
    @app.get("/health")
    def health(detail: bool = Query(False, description="Return detailed diagnostic info")):
        """Return a small health/readiness report.

        - By default returns a compact status and uptime in seconds.
        - If ?detail=true is provided, includes environment checks and platform info.
        """
        uptime = int(time.time() - START_TIME)

        hf_token_present = bool(os.getenv("MINDLY_TOKEN"))
        gen_mode = os.getenv("GEN_MODEL_MODE", "hf")
        ollama_check = {"ok": None, "hint": "not checked"}

        if gen_mode == "local":
            host = os.getenv("OLLAMA_HOST", "localhost")
            try:
                port = int(os.getenv("OLLAMA_PORT", "11434"))
            except Exception:
                port = 11434

            try:
                # quick TCP connect to validate reachability
                with socket.create_connection((host, port), timeout=0.5):
                    ollama_check = {"ok": True, "host": host, "port": port, "hint": "reachable"}
            except Exception as e:
                ollama_check = {"ok": False, "host": host, "port": port, "hint": f"unreachable: {e}"}
        else:
            ollama_check = {"ok": None, "hint": "not used (GEN_MODEL_MODE!=local)"}

        status = "healthy"
        if gen_mode == "hf" and not hf_token_present:
            status = "degraded"
        if gen_mode == "local" and ollama_check.get("ok") is False:
            status = "degraded"

        result = {"status": status, "uptime_seconds": uptime}

        if detail:
            result["checks"] = {
                "hf_token": {"ok": hf_token_present, "hint": "MINDLY_TOKEN present" if hf_token_present else "MINDLY_TOKEN missing"},
                "gen_model_mode": {"mode": gen_mode},
                "ollama": ollama_check,
            }
            result["python"] = {"version": sys.version.split()[0], "platform": platform.platform()}

        return result
