"""
Cloud Run Service — Contact Message Processor
==============================================

Responsibilities:
  1. Decode the Pub/Sub CloudEvent payload
  2. Idempotency check via Firestore (prevents duplicate processing on retry)
  3. Mark the message as processed in Firestore

Environment variables required (set via --set-env-vars or Secret Manager):
  GCP_PROJECT_ID     — GCP project ID
"""

import base64
import json
import logging
import os
from datetime import datetime, timezone

import functions_framework
from google.cloud import firestore

# ── Clients (module-level for connection reuse across warm invocations) ────────
_db: firestore.Client | None = None

IDEMPOTENCY_COLLECTION = "processed_contact_messages"

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _get_db() -> firestore.Client:
    global _db
    if _db is None:
        _db = firestore.Client(project=os.environ["GCP_PROJECT_ID"])
    return _db


# ── Idempotency helpers ────────────────────────────────────────────────────────

def _is_processed(message_id: str) -> bool:
    """Return True if this message_id has already been handled."""
    doc = _get_db().collection(IDEMPOTENCY_COLLECTION).document(message_id).get()
    return doc.exists


def _mark_processed(message_id: str, payload: dict) -> None:
    """Record the message_id so duplicate deliveries are skipped."""
    _get_db().collection(IDEMPOTENCY_COLLECTION).document(message_id).set(
        {
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "name": payload.get("name", ""),
            "email": payload.get("email", ""),
        }
    )


# ── Cloud Run entry point ─────────────────────────────────────────────────────

@functions_framework.cloud_event
def handle_contact_message(cloud_event) -> None:
    """
    EventArc / Pub/Sub CloudEvent handler.
    Pub/Sub wraps the payload under cloud_event.data["message"].
    """
    raw_message = cloud_event.data.get("message", {})
    message_id  = raw_message.get("messageId", "unknown")

    log.info("Received Pub/Sub message: %s", message_id)

    # ── Idempotency: skip if already handled ──────────────────────────────────
    if _is_processed(message_id):
        log.info("Message %s already processed — skipping.", message_id)
        return  # acknowledge without action; Pub/Sub won't redeliver

    # ── Decode base64 payload ─────────────────────────────────────────────────
    data_b64 = raw_message.get("data", "")
    if not data_b64:
        raise ValueError(f"Message {message_id} has no data field.")

    try:
        payload: dict = json.loads(base64.b64decode(data_b64).decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        # Malformed JSON — raising causes Pub/Sub to retry → DLQ after max retries
        raise ValueError(f"Could not decode message {message_id}: {exc}") from exc

    # ── Validate required fields ──────────────────────────────────────────────
    required = {"name", "email", "message", "timestamp"}
    missing  = required - payload.keys()
    if missing:
        raise ValueError(f"Message {message_id} missing fields: {missing}")

    # ── Mark processed (idempotency) ──────────────────────────────────────────
    _mark_processed(message_id, payload)
