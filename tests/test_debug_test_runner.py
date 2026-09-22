from engine.debugging.test_runner import DebugTestRunner


def test_python_correct_output():
    runner = DebugTestRunner()

    result = runner.run_test(
        code="""
a, b = map(int, input().split())
print(a + b)
""",
        language="python",
        input_data="10 20",
        expected_output="30"
    )

    assert result.passed is True
    assert result.status == "passed"
    assert result.expected_output == "30"
    assert result.actual_output == "30"
    assert result.stderr == ""

def test_python_wrong_answer():
    runner = DebugTestRunner()

    result = runner.run_test(
        code="""
a, b = map(int, input().split())
print(a - b)
""",
        language="python",
        input_data="10 20",
        expected_output="30"
    )

    assert result.passed is False
    assert result.status == "wrong_answer"
    assert result.expected_output == "30"
    assert result.actual_output == "-10"
    assert result.stderr == ""

def test_python_runtime_error():
    runner = DebugTestRunner()

    result = runner.run_test(
        code="""
x = 10
y = 0
print(x / y)
""",
        language="python",
        input_data="",
        expected_output="5"
    )

    assert result.passed is False
    assert result.status == "runtime_error"
    assert result.expected_output == "5"
    assert result.actual_output == ""
    assert result.stderr != ""

def test_python_timeout():
    runner = DebugTestRunner()

    result = runner.run_test(
        code="""
while True:
    pass
""",
        language="python",
        input_data="",
        expected_output="anything"
    )

    assert result.passed is False
    assert result.status == "timeout"
    assert result.expected_output == "anything"
    assert result.actual_output == ""