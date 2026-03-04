import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

APP_DIR = Path(__file__).resolve().parents[1] / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from main import app


client = TestClient(app)


def test_root_uses_dev_html_when_app_env_is_dev(monkeypatch):
    monkeypatch.setenv("APP_ENV", "dev")

    response = client.get("/")

    assert response.status_code == 200
    assert "Hello GitOps - DEV" in response.text


def test_root_uses_prod_html_when_app_env_is_prod(monkeypatch):
    monkeypatch.setenv("APP_ENV", "prod")

    response = client.get("/")

    assert response.status_code == 200
    assert "Hello GitOps - PROD" in response.text


def test_root_falls_back_to_default_html_for_unknown_env(monkeypatch):
    monkeypatch.setenv("APP_ENV", "qa")

    response = client.get("/")

    assert response.status_code == 200
    assert "FastAPI is now serving this index.html file" in response.text


def test_root_defaults_to_dev_when_app_env_not_set(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)

    response = client.get("/")

    assert response.status_code == 200
    assert "Hello GitOps - DEV" in response.text
