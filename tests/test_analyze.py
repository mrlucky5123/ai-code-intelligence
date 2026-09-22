from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_analyze_python_success():

    response = client.post(
        "/api/v1/analyze",
        json={
            "code": """
a, b = map(int, input().split())
print(a + b)
""",
            "language": "python",
            "input": "10 20",
            "expected_output": "30"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["status"] == "passed"
    assert data["expected_output"] == "30"
    assert data["actual_output"] == "30"
    assert data["explanation"] is None

def test_analyze_python_wrong_answer(monkeypatch):

    class FakeGroqProvider:

        def explain_failure(self, context):
            from engine.ai.models import DebugExplanation

            return DebugExplanation(
                what_went_wrong="The program subtracts instead of adding.",
                why_it_happened="The code uses a - b.",
                responsible_code="print(a - b)"
            )

    monkeypatch.setattr(
        "backend.app.api.routes.analyze.GroqProvider",
        FakeGroqProvider
    )

    response = client.post(
        "/api/v1/analyze",
        json={
            "code": """
a, b = map(int, input().split())
print(a - b)
""",
            "language": "python",
            "input": "10 20",
            "expected_output": "30"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is False
    assert data["status"] == "wrong_answer"
    assert data["expected_output"] == "30"
    assert data["actual_output"] == "-10"

    assert data["explanation"] is not None
    assert data["explanation"]["what_went_wrong"] == \
        "The program subtracts instead of adding."

def test_analyze_python_runtime_error(monkeypatch):

    class FakeGroqProvider:

        def explain_failure(self, context):
            from engine.ai.models import DebugExplanation

            return DebugExplanation(
                what_went_wrong="The program divides by zero.",
                why_it_happened="The value of y is zero when division occurs.",
                responsible_code="print(x / y)"
            )

    monkeypatch.setattr(
        "backend.app.api.routes.analyze.GroqProvider",
        FakeGroqProvider
    )

    response = client.post(
        "/api/v1/analyze",
        json={
            "code": """
x = 10
y = 0
print(x / y)
""",
            "language": "python",
            "input": "",
            "expected_output": "5"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is False
    assert data["status"] == "runtime_error"
    assert data["expected_output"] == "5"
    assert data["actual_output"] == ""
    assert data["explanation"] is not None