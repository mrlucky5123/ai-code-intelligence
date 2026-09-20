from dataclasses import dataclass


@dataclass
class DebugContext:
    code: str
    language: str
    input_data: str
    expected_output: str
    actual_output: str
    status: str
    stderr: str = ""


@dataclass
class DebugExplanation:
    explanation: str