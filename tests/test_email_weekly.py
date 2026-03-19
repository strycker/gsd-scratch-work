"""Tests for trading_crab_lib.email helpers (Phase 7)."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch, ANY

from trading_crab_lib import OUTPUT_DIR
from trading_crab_lib.email import (
    build_weekly_email_body,
    load_email_config,
    send_weekly_email,
)


class TestLoadEmailConfig:
    def test_missing_file_returns_empty(self, tmp_path):
        cfg = load_email_config(path=tmp_path / "missing.yaml")
        assert cfg == {}

    def test_malformed_file_returns_empty(self, tmp_path):
        path = tmp_path / "email.yaml"
        path.write_text("[]", encoding="utf-8")  # not a mapping
        cfg = load_email_config(path=path)
        assert cfg == {}

    def test_missing_keys_returns_empty(self, tmp_path):
        path = tmp_path / "email.yaml"
        path.write_text("smtp_host: smtp.gmail.com\n", encoding="utf-8")
        cfg = load_email_config(path=path)
        assert cfg == {}

    def test_valid_config_loaded(self, tmp_path):
        path = tmp_path / "email.yaml"
        path.write_text(
            "smtp_host: smtp.gmail.com\n"
            "smtp_port: 587\n"
            "username: user@example.com\n"
            "password: secret\n"
            "from_address: from@example.com\n"
            "to_address: to@example.com\n",
            encoding="utf-8",
        )
        cfg = load_email_config(path=path)
        assert cfg["smtp_host"] == "smtp.gmail.com"
        assert cfg["smtp_port"] == 587
        assert cfg["from_address"] == "from@example.com"
        assert cfg["to_address"] == "to@example.com"


class TestBuildWeeklyEmailBody:
    def test_prefers_email_body_txt(self, tmp_path):
        body_path = tmp_path / "email_body.txt"
        body_path.write_text("plain body", encoding="utf-8")
        report_path = tmp_path / "weekly_report.md"
        report_path.write_text("markdown body", encoding="utf-8")

        subject, body = build_weekly_email_body(tmp_path)
        today = date.today().isoformat()
        assert today in subject
        assert body == "plain body"

    def test_falls_back_to_weekly_report(self, tmp_path):
        report_path = tmp_path / "weekly_report.md"
        report_path.write_text("markdown body", encoding="utf-8")

        subject, body = build_weekly_email_body(tmp_path)
        assert body == "markdown body"


class TestSendWeeklyEmail:
    def test_missing_core_fields_returns_false(self):
        ok = send_weekly_email({}, "subj", "body")
        assert ok is False

    def test_send_with_tls_uses_smtp_and_starttls(self, monkeypatch):
        cfg = {
            "smtp_host": "smtp.test",
            "smtp_port": 587,
            "username": "u",
            "password": "p",
            "use_tls": True,
            "use_ssl": False,
            "from_address": "from@test",
            "to_address": "to@test",
        }
        smtp_mock = MagicMock()
        monkeypatch.setattr("trading_crab_lib.email.smtplib.SMTP", smtp_mock)

        ok = send_weekly_email(cfg, "subj", "body")
        assert ok is True
        smtp_mock.assert_called_once_with("smtp.test", 587)
        instance = smtp_mock.return_value.__enter__.return_value
        assert instance.starttls.called
        assert instance.login.called
        assert instance.send_message.called

    def test_send_with_ssl_uses_smtp_ssl(self, monkeypatch):
        cfg = {
            "smtp_host": "smtp.test",
            "smtp_port": 465,
            "username": "u",
            "password": "p",
            "use_tls": False,
            "use_ssl": True,
            "from_address": "from@test",
            "to_address": "to@test",
        }
        smtp_ssl_mock = MagicMock()
        monkeypatch.setattr("trading_crab_lib.email.smtplib.SMTP_SSL", smtp_ssl_mock)

        ok = send_weekly_email(cfg, "subj", "body")
        assert ok is True
        smtp_ssl_mock.assert_called_once_with("smtp.test", 465, context=ANY)
        instance = smtp_ssl_mock.return_value.__enter__.return_value
        assert instance.login.called
        assert instance.send_message.called

