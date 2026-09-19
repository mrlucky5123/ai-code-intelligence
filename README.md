# AI Code Intelligence

An intelligent code analysis and debugging platform designed to understand, execute, analyze, and explain source code.

The project is being built incrementally, starting with a secure code execution foundation and evolving toward an intelligent analysis and debugging system capable of combining program execution, static analysis, and AI-powered reasoning.

---

## 🚧 Project Status

**Current Phase:** Secure Code Execution Engine

The project currently provides:

* FastAPI-based backend
* Source-code validation
* C++ compilation and execution
* Docker-isolated code execution
* Compile-error detection
* Runtime-error detection
* Execution timeout handling
* Resource restrictions
* Container cleanup
* Automated testing
* REST API for code analysis requests

The AI-powered code intelligence layer is planned as the next major stage of development.

---

# 🎯 Problem Statement

When a programmer encounters a bug, the problem is usually not simply finding that the program failed.

A useful debugging system should answer questions such as:

* Did the code compile?
* If compilation failed, what caused the failure?
* If it compiled, did the program crash?
* Did it produce incorrect output?
* Which part of the program is responsible?
* What was the program trying to do?
* Why did the observed behavior differ from the expected behavior?
* How can the programmer fix it?
* How confident is the system in its explanation?

Traditional compilers and execution environments provide valuable raw information, but they do not necessarily transform that information into an understandable explanation.

**AI Code Intelligence** aims to build that layer.

The long-term goal is to create a system that combines:

```text
Source Code
     ↓
Validation
     ↓
Safe Execution
     ↓
Program Evidence
     ↓
Static Analysis
     ↓
Bug / Behavior Analysis
     ↓
AI Reasoning
     ↓
Human-Friendly Explanation
     ↓
Suggested Fix
```

---

# 🧠 Core Idea

The project is intentionally being developed in layers.

Instead of immediately sending code to an LLM and asking it to "find the bug", the system first builds reliable program evidence.

For example:

```text
User Code
   ↓
Does it contain valid input?
   ↓
Can it compile?
   ↓
Can it execute safely?
   ↓
Did it terminate?
   ↓
What output did it produce?
   ↓
What errors occurred?
   ↓
What does static analysis reveal?
   ↓
What can an AI model infer from all this evidence?
```

This separation allows the future AI layer to reason over actual execution and analysis data rather than relying only on the source code.

---

# 🏗️ Current Architecture

```text
                    ┌─────────────────────┐
                    │       Client        │
                    │  Swagger / Frontend │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │       Backend       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Analysis Service  │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
          ┌─────────────────┐   ┌──────────────────┐
          │ Code Validation │   │ Docker Executor  │
          └─────────────────┘   └────────┬─────────┘
                                         │
                                         ▼
                                ┌─────────────────┐
                                │ Docker Sandbox  │
                                │                 │
                                │  g++ compiler   │
                                │  C++ program    │
                                └────────┬────────┘
                                         │
                                         ▼
                                Execution Evidence
```

---

# 🔄 Current Execution Flow

A request to:

```text
POST /api/v1/analyze
```

follows this flow:

```text
1. Receive source code
          ↓
2. Validate request
          ↓
3. Validate language/code
          ↓
4. Create isolated Docker container
          ↓
5. Compile C++ source
          ↓
6. If compilation fails → compile_error
          ↓
7. If compilation succeeds → execute
          ↓
8. If execution succeeds → success
          ↓
9. If program crashes → runtime_error
          ↓
10. If execution exceeds timeout → timeout
          ↓
11. Remove container
          ↓
12. Return structured JSON response
```

---

# 🐳 Docker Execution Sandbox

Arbitrary source code should not be executed directly on the host machine.

The current execution engine therefore runs submitted C++ programs inside Docker.

The sandbox currently applies multiple restrictions:

### Network isolation

```text
--network none
```

The container has no network access.

### CPU restriction

```text
--cpus 1
```

The container is limited to one CPU.

### Memory restriction

```text
--memory 256m
```

The container has a memory limit.

### Process restriction

```text
--pids-limit 64
```

Limits the number of processes that can be created.

### Linux capability restrictions

```text
--cap-drop ALL
```

Linux capabilities are dropped from the container.

### Privilege restriction

```text
--security-opt no-new-privileges:true
```

Prevents processes from gaining additional privileges.

### Read-only filesystem

```text
--read-only
```

The container's root filesystem is read-only.

### Read-only source workspace

```text
/workspace:ro
```

Submitted source code is mounted read-only.

### Controlled temporary filesystem

```text
/tmp
```

A limited writable temporary filesystem is provided for compilation and execution.

### Container cleanup

Containers are removed after execution, including timeout paths.

The goal is to establish multiple layers of isolation rather than relying on a single security mechanism.

---

# ⚙️ Execution State Machine

The executor distinguishes compilation from execution.

```text
                Source Code
                     │
                     ▼
                  Compile
                 /       \
                /         \
             FAIL          SUCCESS
              │               │
              ▼               ▼
       compile_error        Execute
                           /   |    \
                          /    |     \
                       success crash timeout
                          │      │       │
                          ▼      ▼       ▼
                       success runtime  timeout
                                error
```

This distinction is important.

For example:

```cpp
int main() {
    return 100;
}
```

is a successfully compiled program.

Its exit code is `100`, but that does not mean compilation failed.

Therefore the system determines the execution **stage** first and interprets the result within that stage.

---

# 📁 Project Structure

```text
ai-code-intelligence/
│
├── backend/
│   └── app/
│       ├── main.py
│       │
│       ├── api/
│       │   └── routes/
│       │       ├── health.py
│       │       └── analyze.py
│       │
│       └── services/
│           └── analyze_service.py
│
├── engine/
│   ├── validation/
│   │   └── code_validator.py
│   │
│   └── execution/
│       ├── executor.py
│       └── docker_executor.py
│
├── tests/
│   ├── fixtures/
│   │   ├── hello.cpp
│   │   ├── compile_error.cpp
│   │   ├── runtime_error.cpp
│   │   └── infinite_loop.cpp
│   │
│   ├── test_analyze_service.py
│   ├── test_code_validator.py
│   ├── test_docker_executor.py
│   └── test_executor.py
│
├── Dockerfile
├── README.md
├── backend/requirements.txt
└── .gitignore
```

`executor.py` represents the earlier host-based execution approach and is preserved as part of the project's development history.

The active execution path uses `docker_executor.py`.

---

# 🧩 Backend Components

## FastAPI Application

`backend/app/main.py`

Responsible for:

* Creating the FastAPI application
* Registering API routes
* Providing the application entry point

---

## API Routes

### Health Check

```text
GET /api/v1/health
```

Used to verify that the backend is running.

Example response:

```json
{
  "status": "ok"
}
```

### Code Analysis

```text
POST /api/v1/analyze
```

Accepts:

```json
{
  "code": "<source code>",
  "language": "cpp"
}
```

The request is passed to the analysis service.

---

## Code Validation

`engine/validation/code_validator.py`

Currently validates:

* Whether source code is empty
* Whether the requested language is supported

Currently supported language:

```text
C++
```

Additional languages can be added later.

---

## Analysis Service

`backend/app/services/analyze_service.py`

Acts as the orchestration layer.

Its responsibility is to coordinate:

```text
Validation
    ↓
Execution
    ↓
Result interpretation
    ↓
API response
```

The service does not contain Docker implementation details.

This separation allows the execution implementation to evolve independently.

---

## Docker Code Executor

`engine/execution/docker_executor.py`

Responsible for:

* Creating a temporary source workspace
* Creating a restricted Docker container
* Starting the container
* Compiling submitted C++ code
* Executing the compiled program
* Capturing stdout/stderr
* Detecting runtime failures
* Detecting timeouts
* Cleaning up the container

The executor returns structured execution information rather than directly deciding how the API should describe the result.

---

# 📊 Execution Result

The execution engine produces information such as:

```json
{
  "stdout": "...",
  "stderr": "...",
  "exit_code": 0,
  "timed_out": false,
  "stage": "success"
}
```

The analysis service converts execution stages into API-level statuses.

Current statuses include:

```text
validation_error
compile_error
runtime_error
timeout
success
```

---

# 🧪 Testing

The project currently has automated tests covering:

* Code validation
* Valid C++ execution
* Compilation failures
* Runtime failures
* Non-zero program exit codes
* Infinite loops
* Execution timeouts
* Read-only workspace enforcement
* Normal container cleanup
* Timeout container cleanup
* Analysis service integration

Current test suite:

```text
16 tests
16 passed
```

Run the test suite with:

```bash
python -m pytest -v
```

---

# 🚀 Running the Project Locally

## 1. Create and activate the virtual environment

```bash
python -m venv .venv
source .venv/Scripts/activate
```

## 2. Install dependencies

```bash
python -m pip install -r backend/requirements.txt
```

## 3. Build the C++ execution image

```bash
docker build -t cpp-execution-image .
```

## 4. Start the FastAPI server

```bash
python -m uvicorn backend.app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🛠️ Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

### Code Execution

* C++
* GCC / g++
* Docker

### Testing

* pytest

### Development

* Git
* GitHub
* VS Code

---

# 🗺️ Development Roadmap

The roadmap is intentionally ordered by **architectural importance and the strength of the final project story**, rather than simply adding random features.

## Phase 1 — Secure Execution Foundation

**Status: ✅ Complete**

* [x] FastAPI backend
* [x] Code validation
* [x] C++ compilation
* [x] C++ execution
* [x] Docker isolation
* [x] Resource restrictions
* [x] Timeout handling
* [x] Structured execution results
* [x] Automated tests
* [x] API integration

---

## Phase 2 — Static Code Analysis

**Priority: 🔥 High**

Introduce analysis that does not require executing the program.

Planned capabilities:

* [ ] Syntax-aware code analysis
* [ ] AST-based analysis
* [ ] Detection of suspicious code patterns
* [ ] Complexity estimation
* [ ] Basic code-quality analysis
* [ ] Identification of potentially problematic constructs

Goal:

```text
Source Code
     ↓
Static Analysis
     ↓
Structured Code Facts
```

---

## Phase 3 — Program Behavior & Test Evaluation

**Priority: 🔥 High**

Move beyond "does it run?" toward "does it behave correctly?"

Planned capabilities:

* [ ] User-provided test cases
* [ ] Automated test execution
* [ ] Expected-vs-actual output comparison
* [ ] Multiple test-case execution
* [ ] Failure isolation
* [ ] Structured test reports

Goal:

```text
Code
 ↓
Test Cases
 ↓
Sandboxed Execution
 ↓
Expected vs Actual
 ↓
Failure Evidence
```

---

## Phase 4 — Intelligent Bug Detection

**Priority: 🔥🔥 Very High**

Combine source code, static analysis, and execution evidence.

Planned capabilities:

* [ ] Bug classification
* [ ] Error localization
* [ ] Suspicious-line identification
* [ ] Runtime evidence analysis
* [ ] Root-cause reasoning
* [ ] Confidence estimation

Goal:

```text
Code
 +
Compiler Evidence
 +
Runtime Evidence
 +
Static Analysis
        ↓
Bug Analysis
```

---

## Phase 5 — AI-Powered Explanation

**Priority: 🔥🔥 Very High**

Introduce an LLM as a reasoning and explanation layer.

The AI should receive structured evidence rather than blindly analyzing raw code alone.

Planned capabilities:

* [ ] LLM integration
* [ ] Context-aware debugging explanations
* [ ] Root-cause explanations
* [ ] Step-by-step reasoning for developers
* [ ] Suggested corrections
* [ ] Explanation of compiler/runtime errors

Goal:

```text
Program Evidence
       +
Static Analysis
       +
Source Code
       ↓
      LLM
       ↓
Human-Friendly Explanation
```

---

## Phase 6 — Automated Fix Suggestions

**Priority: 🔥🔥 Very High**

Move from explaining problems to helping solve them.

Planned capabilities:

* [ ] Generate candidate fixes
* [ ] Show code diffs
* [ ] Recompile generated fixes
* [ ] Re-run failing tests
* [ ] Verify whether the proposed fix actually works

Potential feedback loop:

```text
Bug
 ↓
Generate Fix
 ↓
Compile
 ↓
Run Tests
 ↓
Pass?
 ├── No → Refine Fix
 └── Yes → Present Fix
```

This verification loop is intended to make the system more reliable than an AI that simply produces an unverified code suggestion.

---

## Phase 7 — Code Intelligence Dashboard

**Priority: High**

Build a frontend around the analysis engine.

Planned capabilities:

* [ ] Code editor
* [ ] Execution controls
* [ ] Test-case interface
* [ ] Error visualization
* [ ] Static-analysis results
* [ ] AI explanations
* [ ] Suggested fixes
* [ ] Execution history

Long-term interaction:

```text
┌─────────────────────────────────────────────┐
│                Code Editor                  │
├─────────────────────────────────────────────┤
│                                             │
│              User Source Code               │
│                                             │
├─────────────────────────────────────────────┤
│ Analysis │ Tests │ Runtime │ AI Explanation │
└─────────────────────────────────────────────┘
```

---

## Phase 8 — Scalable Execution Architecture

**Priority: High for production readiness**

The current Docker executor is designed as a strong local foundation.

A larger deployment can evolve toward:

```text
Frontend
    ↓
FastAPI
    ↓
Job Queue
    ↓
Execution Workers
    ↓
Docker Sandboxes
```

Planned capabilities:

* [ ] Background jobs
* [ ] Queue-based execution
* [ ] Worker processes
* [ ] Concurrent execution
* [ ] Job status tracking
* [ ] Persistent analysis history
* [ ] Observability and logging

---

# 🔮 Long-Term Vision

The final system should behave less like a compiler wrapper and more like an intelligent debugging assistant.

A possible end-to-end interaction:

```text
Developer submits code
        ↓
System validates code
        ↓
System safely executes it
        ↓
System runs test cases
        ↓
Static analyzer examines source
        ↓
Execution engine collects evidence
        ↓
Analysis engine identifies likely problem
        ↓
AI explains the root cause
        ↓
AI proposes a fix
        ↓
System verifies the fix
        ↓
Developer receives:
    • What went wrong
    • Why it went wrong
    • Where it went wrong
    • How to fix it
    • Whether the fix was verified
```

---

# 📈 Project Evolution

This project is being developed incrementally.

### Stage 1 — Basic backend

```text
FastAPI
  ↓
Validation
  ↓
Local execution
```

### Stage 2 — Structured execution

```text
FastAPI
  ↓
Validation
  ↓
Compile
  ↓
Execute
  ↓
Structured result
```

### Stage 3 — Isolated execution

```text
FastAPI
  ↓
Validation
  ↓
Docker Executor
  ↓
Restricted Sandbox
  ↓
Compile + Execute
```

### Stage 4 — Planned intelligence layer

```text
Code
 ↓
Secure Execution
 ↓
Static Analysis
 ↓
Behavior Analysis
 ↓
AI Reasoning
 ↓
Explanation
 ↓
Verified Fix
```

The architecture is intentionally evolving from **reliable execution → reliable evidence → intelligent reasoning**.

---

# 🎓 Engineering Principles

The project follows several principles throughout development:

### 1. Separate responsibilities

Validation, execution, orchestration, analysis, and AI reasoning should remain separate components.

### 2. Prefer evidence over assumptions

The future intelligence layer should use compiler output, runtime behavior, test results, and static-analysis information wherever possible.

### 3. Never trust submitted code

User-provided source code should be treated as untrusted input and executed inside an isolated environment.

### 4. Verify generated fixes

An AI-generated fix should ideally be compiled and tested before being presented as a verified solution.

### 5. Build incrementally

Each architectural layer should be independently testable before the next layer is added.

### 6. Preserve architectural history

Earlier implementations are preserved where useful so that design decisions and evolution can be understood rather than hidden.

---

# 📌 Current Milestone

**Secure Docker-Based Code Execution**

The current implementation has established the foundation required for the next stage: collecting richer program evidence and building the actual intelligence layer on top of it.
