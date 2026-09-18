from backend.app.services.analyze_service import analyze_code


def test_valid_code():
    result = analyze_code("int main() { return 0; }", "cpp")

    assert result == {
        "success": True,
        "status": "success",
        "language": "cpp",
        "stdout": "",
        "stderr": "",
        "exit_code": 0,
        "timed_out": False
    }


def test_empty_code():
    result = analyze_code("", "cpp")

    assert result == {
        "success": False,
        "status": "validation_error",
        "message": "Code cannot be empty.",
        "language": "cpp"
    }


def test_unsupported_language():
    result = analyze_code("print('Hello')", "python")

    assert result == {
        "success": False,
        "status": "validation_error",
        "message": "Unsupported language: python",
        "language": "python"
    }


def test_compile_error():
    result = analyze_code(
        """
#include <iostream>

int main() {
    std::cout << "Hello"
    return 0;
}
""",
        "cpp"
    )

    assert result["success"] is False
    assert result["status"] == "compile_error"
    assert result["exit_code"] != 0
    assert result["stderr"] != ""
    assert result["timed_out"] is False


def test_timeout():
    result = analyze_code(
        """
int main() {
    while (true) {
    }

    return 0;
}
""",
        "cpp"
    )

    assert result["success"] is False
    assert result["status"] == "timeout"
    assert result["timed_out"] is True