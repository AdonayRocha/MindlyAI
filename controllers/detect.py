from models.req import Req

def register(app, detect_alerts, simple_topic_extraction, compute_risk_basic):
    @app.post("/detect")
    def detect(req: Req):
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
