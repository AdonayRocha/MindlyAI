from fastapi import FastAPI, HTTPException, Header
from models.req import Req
from dotenv import load_dotenv
import os
from groq import Groq
from typing import List
from keywords.alerts import ALERTS
from keywords.topics import TOPIC_KEYWORDS
from controllers import speak, detect, health, analyze

load_dotenv()

ALLOWED = os.getenv("API_KEYS", "meu_token").split(",")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


app = FastAPI(title="Mindly")

# Helper functions for detect
def detect_alerts(text):
	return [a for a in ALERTS if a in text.lower()]

def simple_topic_extraction(text):
	found = []
	for topic, keywords in TOPIC_KEYWORDS.items():
		if any(k in text.lower() for k in keywords):
			found.append(topic)
	return found

def compute_risk_basic(alerts, topics):
	score = 0
	if alerts:
		score += 5
	score += len(topics)
	return score

analyze.register(app, ALLOWED)
speak.register(app, ALLOWED)
detect.register(app, detect_alerts, simple_topic_extraction, compute_risk_basic)
health.register(app)
