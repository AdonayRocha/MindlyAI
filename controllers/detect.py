from fastapi import FastAPI
from typing import Any


def register(app: FastAPI, Req, detect_alerts, simple_topic_extraction, compute_risk_basic):
    @app.post("/detect")
    def detect(req: Any):
        # FastAPI will provide the body as a dict when annotation is generic; convert to Req for convenience
        if not isinstance(req, Req):
            try:
                req = Req.parse_obj(req)
            except Exception:
                # If conversion fails, fallback to a minimal object-like dict
                req = type("_R", (), {"text": (req.get("text") if isinstance(req, dict) else ""), "meta": {}})()

        text = req.text or ""
        alerts = detect_alerts(text)
        topics = simple_topic_extraction(text)
        risk = compute_risk_basic(alerts, topics)
        return {
            "alert": bool(alerts),
            "alert_words": alerts,
            "topics": topics,
            "risk_score": risk
        }
