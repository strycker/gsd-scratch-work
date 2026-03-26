"""
SMTP helpers for optional weekly report delivery.

Secrets live only in ``config/email.local.yaml`` (gitignored). Sending is
opt-in; failures are logged and must not abort the pipeline.
"""

from __future__ import annotations

import logging
import smtplib
import ssl
from datetime import date
from email.message import EmailMessage
from pathlib import Path

import yaml

from trading_crab_lib import CONFIG_DIR, OUTPUT_DIR

log = logging.getLogger(__name__)

EMAIL_CONFIG_NAME = "email.local.yaml"


def load_email_config(path: Path | None = None) -> dict:
    """
    Load SMTP/email config from YAML.

    Default location: CONFIG_DIR / email.local.yaml
    Returns {} if the file is missing or malformed.
    """
    cfg_path = path or (CONFIG_DIR / EMAIL_CONFIG_NAME)
    if not cfg_path.exists():
        log.info("Email config %s not found; email sending is disabled.", cfg_path)
        return {}
    try:
        with open(cfg_path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            log.warning("Email config %s is not a mapping; ignoring.", cfg_path)
            return {}
        required = {"smtp_host", "smtp_port", "username", "password", "from_address", "to_address"}
        if not required.issubset(data.keys()):
            missing = required - set(data.keys())
            log.warning("Email config %s missing keys: %s", cfg_path, ", ".join(sorted(missing)))
            return {}
        return data
    except Exception as exc:  # pragma: no cover - defensive
        log.warning("Failed to read email config %s: %s", cfg_path, exc)
        return {}


def build_weekly_email_body(reports_dir: Path | None = None) -> tuple[str, str]:
    """
    Build (subject, body) for the weekly email.

    Prefer outputs/reports/email_body.txt, fall back to weekly_report.md.
    """
    reports = reports_dir or (OUTPUT_DIR / "reports")
    body_path = reports / "email_body.txt"
    report_path = reports / "weekly_report.md"

    if body_path.exists():
        body = body_path.read_text(encoding="utf-8")
    elif report_path.exists():
        body = report_path.read_text(encoding="utf-8")
    else:
        body = "Weekly report not found; no content available."

    today = date.today().isoformat()
    subject = f"Trading-Crab Weekly Report — {today}"
    return subject, body


def _build_message(config: dict, subject: str, body: str) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = config["from_address"]
    msg["To"] = config["to_address"]
    msg.set_content(body)
    return msg


def send_weekly_email(config: dict, subject: str, body: str) -> bool:
    """
    Send the weekly email using the provided config and content.

    Returns True on success, False on failure.
    """
    host = config.get("smtp_host")
    port = int(config.get("smtp_port", 0) or 0)
    username = config.get("username")
    password = config.get("password")
    use_tls = bool(config.get("use_tls", False))
    use_ssl = bool(config.get("use_ssl", False))

    if not host or not port or not username or not password:
        log.warning("Email config missing host/port/username/password; skipping send.")
        return False

    msg = _build_message(config, subject, body)

    try:
        if use_ssl:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(host, port, context=context) as server:
                server.login(username, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(host, port) as server:
                server.ehlo()
                if use_tls:
                    context = ssl.create_default_context()
                    server.starttls(context=context)
                    server.ehlo()
                server.login(username, password)
                server.send_message(msg)
        log.info("Weekly email sent to %s via %s:%s", config.get("to_address"), host, port)
        return True
    except Exception as exc:  # pragma: no cover - network/SMTP dependent
        log.warning("Failed to send weekly email: %s", exc)
        return False
