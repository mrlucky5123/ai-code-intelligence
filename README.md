# AI Code Intelligence

AI Code Intelligence is a small FastAPI service and execution engine for validating and running C++ code. It accepts source code through an HTTP API, checks that the request is supported, compiles the program, executes it with a five-second timeout, and reports whether it succeeded, failed to compile, failed at runtime, or timed out.

> **Current scope:** C++ is the only supported language.

## Features

- FastAPI HTTP API with versioned routes under `/api/v1`
- Empty-code and unsupported-language validation
- C++ compilation with `g++`
- Native execution through `CodeExecutor`
- Isolated Docker execution through `DockerCodeExecutor`
- Docker execution limits:
  - No network access
  - 1 CPU and 256 MB memory
  - Maximum of 64 processes
  - Dropped Linux capabilities
  - Read-only container filesystem
  - Read-only source workspace
  - Five-second execution timeout
- Structured results for validation, compilation, runtime, and timeout failures
- Pytest coverage for the validator, service layer, native executor, and Docker executor

## Architecture

```text
backend/app/api/routes/analyze.py
        │ POST /api/v1/analyze
        ▼
backend/app/services/analyze_service.py
        │ validate_code()
        │ DockerCodeExecutor.execute()
        ▼
engine/validation/code_validator.py
engine/execution/docker_executor.py
        │
        ├── compile with g++
        └── run the compiled program
```

The API layer defines the request model and delegates work to `analyze_code`. The service validates the request, invokes the Docker-backed executor, and maps executor stages to API statuses. The `engine/execution/executor.py` implementation provides a simpler local execution path that compiles and runs C++ directly on the host.

## Repository layout

```text
backend/
  app/
    main.py                    FastAPI application entry point
    api/routes/                Health and code-analysis HTTP routes
    services/analyze_service.py Validation and execution orchestration
  requirements.txt             Python dependencies
engine/
  validation/code_validator.py Supported-language and empty-code checks
  execution/executor.py        Native host compiler/executor
  execution/docker_executor.py Sandboxed Docker compiler/executor
tests/
  fixtures/                    C++ examples for success and failure cases
  test_analyze_service.py     Service behavior tests
  test_code_validator.py      Validation tests
  test_executor.py             Native executor tests
  test_docker_executor.py      Docker isolation and cleanup tests
Dockerfile                     Builds the C++ execution image
```

## Requirements

- Python 3.10+
- `pip`
- `g++` for native execution tests
- Docker Engine for Docker-backed execution and Docker tests

The Docker executor expects an image named `cpp-execution-image`. Build it from the repository's `Dockerfile` before using that executor:

```bash
docker build -t cpp-execution-image .
```

## Setup

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r backend/requirements.txt
```

## Run the API

Start Uvicorn from the repository root:

```bash
uvicorn backend.app.main:app --reload
```

The service is then available at `http://127.0.0.1:8000`.

### Health check

```bash
curl http://127.0.0.1:8000/api/v1/health
```

Expected response:

```json
{"status":"ok"}
```

### Analyze C++ code

```bash
curl -X POST http://127.0.0.1:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"language":"cpp","code":"#include <iostream>\nint main() { std::cout << \\"Hello\\"; return 0; }"}'
```

A successful response has the following shape:

```json
{
  "success": true,
  "status": "success",
  "language": "cpp",
  "stdout": "Hello",
  "stderr": "",
  "exit_code": 0,
  "timed_out": false
}
```

Possible statuses include:

- `validation_error` — empty source or unsupported language
- `compile_error` — `g++` could not compile the source
- `runtime_error` — the compiled program exited with a non-zero code
- `timeout` — execution exceeded five seconds
- `success` — compilation and execution completed successfully

## Run tests

Run the full test suite:

```bash
pytest
```

For tests that use Docker, make sure the execution image has been built first:

```bash
docker build -t cpp-execution-image .
pytest tests/test_docker_executor.py
```

The Docker tests verify successful execution, compile errors, runtime errors, timeouts, read-only workspace behavior, and container cleanup.

## Security note

The Docker executor is designed to reduce the risk of running untrusted C++ by disabling networking, limiting resources, dropping capabilities, using a read-only filesystem, mounting the workspace read-only, and removing the container in a `finally` block. No sandbox should be treated as a complete security boundary without additional host-level hardening and operational controls.

## License

No license file is currently included in the repository.
