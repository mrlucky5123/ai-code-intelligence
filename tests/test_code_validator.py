from engine.validation.code_validator import validate_code

def test_valid_cpp_code():
    result = validate_code("int main() { return 0; }", "cpp")

    assert result == (True, "Code is valid.")

def test_empty_code():
    result = validate_code("", "cpp")

    assert result == (False, "Code cannot be empty.")

def test_unsupported_language():
    result = validate_code("print('Hello, World!')", "java")

    assert result == (False, "Unsupported language: java")