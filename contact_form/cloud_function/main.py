"""
Cloud Run Service — Contact Form Submission Handler
====================================================

Accepts HTTP POST requests directly from the website contact form,
validates the input, and publishes the message to the Pub/Sub topic.
The BigQuery subscription on that topic handles writing to BigQuery automatically.

Environment variables (set via Cloud Run --set-env-vars or Secret Manager):
  GCP_PROJECT_ID   — GCP project ID
  PUBSUB_TOPIC_ID  — Pub/Sub topic name (default: anwesha-net-msg-topic)
  ALLOWED_ORIGIN   — CORS allowed origin, e.g. https://anwesha.net (default: *)
"""

import json
import logging
import os
import re
from datetime import datetime, timezone

import functions_framework
from flask import Request
from google.cloud import pubsub_v1

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PUBSUB_TOPIC_ID = os.environ.get("PUBSUB_TOPIC_ID", "anwesha-net-msg-topic")

# Module-level client — reused across warm invocations to avoid repeated auth overhead.
_publisher: pubsub_v1.PublisherClient | None = None


def _get_publisher() -> pubsub_v1.PublisherClient:
    global _publisher
    if _publisher is None:
        _publisher = pubsub_v1.PublisherClient()  # keyless — uses ADC / service account
    return _publisher


def _cors_headers() -> dict:
    return {
        "Access-Control-Allow-Origin":  os.environ.get("ALLOWED_ORIGIN", "*"),
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }


@functions_framework.http
def handle_contact_message(request: Request):
    """
    HTTP endpoint called directly by the website contact form (cross-origin).

    Handles CORS preflight, validates the JSON body, publishes to Pub/Sub,
    and returns a JSON response.
    """
    # ── CORS preflight ────────────────────────────────────────────────────────
    if request.method == "OPTIONS":
        return ("", 204, _cors_headers())

    if request.method != "POST":
        return (json.dumps({"error": "Method not allowed"}), 405, _cors_headers())

    # ── Parse body ────────────────────────────────────────────────────────────
    body = request.get_json(silent=True)
    if not body:
        return (json.dumps({"error": "Request body must be valid JSON"}), 400, _cors_headers())

    name    = str(body.get("name",    "")).strip()
    email   = str(body.get("email",   "")).strip()
    message = str(body.get("message", "")).strip()

    # ── Validate ──────────────────────────────────────────────────────────────
    if not all([name, email, message]):
        return (json.dumps({"error": "name, email and message are all required"}), 422, _cors_headers())

    if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
        return (json.dumps({"error": "Invalid email format"}), 422, _cors_headers())

    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        return (json.dumps({"error": "Server misconfiguration"}), 500, _cors_headers())

    # ── Publish to Pub/Sub ────────────────────────────────────────────────────
    payload = {
        "name":      name,
        "email":     email,
        "message":   message,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    try:
        publisher  = _get_publisher()
        topic_path = publisher.topic_path(project_id, PUBSUB_TOPIC_ID)
        future     = publisher.publish(
            topic_path,
            data=json.dumps(payload).encode("utf-8"),
            content_type="application/json",
        )
        message_id = future.result(timeout=10)
    except Exception as exc:
        log.exception("Pub/Sub publish failed: %s", exc)
        return (json.dumps({"error": "Failed to submit message. Please try again."}), 502, _cors_headers())

    log.info("Published message %s to topic %s", message_id, PUBSUB_TOPIC_ID)
    return (
        json.dumps({"status": "sent", "message_id": message_id}),
        200,
        {**_cors_headers(), "Content-Type": "application/json"},
    )
