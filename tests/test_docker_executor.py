from engine.execution.docker_executor import DockerCodeExecutor
import subprocess

def get_executor_containers():
    result = subprocess.run(
        [
            "docker",
            "ps",
            "-aq",
            "--filter",
            "label=ai-code-intelligence.executor=true"
        ],
        capture_output=True,
        text=True
    )

    return result.stdout.strip().splitlines()


def test_docker_valid_code():
    executor = DockerCodeExecutor()

    result = executor.execute(
        """
#include <iostream>

int main() {
    std::cout << "Hello from Docker";
    return 0;
}
""",
        "cpp"
    )

    print(result)

    assert result.stage == "success"
    assert result.exit_code == 0
    assert result.timed_out is False
    assert "Hello from Docker" in result.stdout

def test_docker_compile_error():
    executor = DockerCodeExecutor()

    result = executor.execute(
        """
#include <iostream>

int main() {
    std::cout << "Hello"
    return 0;
}
""",
        "cpp"
    )

    print(result)

    assert result.stage == "compile"
    assert result.timed_out is False
    assert result.exit_code != 0
    assert result.stderr != ""

def test_docker_runtime_error():
    executor = DockerCodeExecutor()

    result = executor.execute(
        """
#include <iostream>

int main() {
    int x = 10;
    int y = 0;

    std::cout << x / y << "\\n";

    return 0;
}
""",
        "cpp"
    )

    print(result)

    assert result.stage == "runtime"
    assert result.timed_out is False
    assert result.exit_code != 0

def test_docker_program_returns_100():
    executor = DockerCodeExecutor()

    result = executor.execute(
        """
int main() {
    return 100;
}
""",
        "cpp"
    )

    print(result)

    assert result.stage == "runtime"
    assert result.exit_code == 100
    assert result.timed_out is False


def test_docker_timeout():
    executor = DockerCodeExecutor()

    result = executor.execute(
        """
int main() {
    while (true) {
    }

    return 0;
}
""",
        "cpp"
    )

    print(result)

    assert result.stage == "timeout"
    assert result.timed_out is True
    assert result.exit_code == -1


def test_docker_workspace_is_read_only():
    executor = DockerCodeExecutor()

    result = executor.execute(
        """
#include <fstream>

int main() {
    std::ofstream file("/workspace/hacked.txt");

    if (file.is_open()) {
        return 0;
    }

    return 1;
}
""",
        "cpp"
    )

    print(result)

    assert result.stage == "runtime"
    assert result.exit_code != 0

def test_docker_container_is_cleaned_up():
    executor = DockerCodeExecutor()

    before = get_executor_containers()

    result = executor.execute(
        """
#include <iostream>

int main() {
    std::cout << "cleanup test";
    return 0;
}
""",
        "cpp"
    )

    print(result)

    after = get_executor_containers()

    assert result.stage == "success"
    assert before == after

def test_docker_timeout_cleans_up_container():
    executor = DockerCodeExecutor()

    before = get_executor_containers()

    result = executor.execute(
        """
int main() {
    while (true) {
    }

    return 0;
}
""",
        "cpp"
    )

    print(result)

    after = get_executor_containers()

    assert result.stage == "timeout"
    assert result.timed_out is True
    assert before == after