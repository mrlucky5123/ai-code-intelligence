# from engine.execution.executor import CodeExecutor


# def test_execute_valid_cpp():
#     executor = CodeExecutor()

#     result = executor.execute(
#         """
# #include <iostream>

# int main() {
#     std::cout << "Hello from executor\\n";
#     return 0;
# }
# """,
#         "cpp"
#     )

#     assert result.stdout == "Hello from executor\n"
#     assert result.stderr == ""
#     assert result.exit_code == 0
#     assert result.timed_out is False
#     assert result.stage == "success"


# def test_execute_compile_error():
#     executor = CodeExecutor()

#     result = executor.execute(
#         """
# #include <iostream>

# int main() {
#     std::cout << "Hello"
#     return 0;
# }
# """,
#         "cpp"
#     )

#     assert result.exit_code != 0
#     assert result.stderr != ""
#     assert result.timed_out is False
#     assert result.stage == "compile"


# def test_execute_unsupported_language():
#     executor = CodeExecutor()

#     result = executor.execute(
#         "print('Hello')",
#         "python"
#     )

#     assert result.exit_code == -1
#     assert result.timed_out is False
#     assert result.stderr == "Unsupported language: python"
#     assert result.stage == "validation"


# def test_execute_timeout():
#     executor = CodeExecutor()

#     result = executor.execute(
#         """
# int main() {
#     while (true) {
#     }

#     return 0;
# }
# """,
#         "cpp"
#     )

#     assert result.timed_out is True
#     assert result.stage == "timeout"