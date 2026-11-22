import importlib
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

FIXED_NOW = datetime(2026, 1, 15, 10, 0, tzinfo=timezone.utc)


class _RedProxy:
    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        raise AssertionError(
            f"RED: {self._target!r} todavía no existe; esta falla es esperada en TDD"
        )


def load_module(name):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError:
        return _RedProxy(name)


@pytest.fixture
def fixed_now():
    return FIXED_NOW


@pytest.fixture
def models():
    return load_module("prestamos.models")


@pytest.fixture
def errors():
    return load_module("prestamos.errors")


@pytest.fixture
def service_factory():
    def build(clock=None):
        service_module = load_module("prestamos.service")
        return service_module.LoanService(clock=clock or (lambda: FIXED_NOW))

    return build


@pytest.fixture
def service():
    service_module = load_module("prestamos.service")
    if isinstance(service_module, _RedProxy):
        return _RedProxy("prestamos.service.LoanService")
    return service_module.LoanService(clock=lambda: FIXED_NOW)


@pytest.fixture
def shell_factory(service_factory):
    def build(service=None):
        cli_module = load_module("prestamos.cli")
        return cli_module.LoanShell(service or service_factory())

    return build
