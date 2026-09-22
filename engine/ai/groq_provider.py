import os

from dotenv import load_dotenv
from groq import Groq
import json

from engine.ai.models import DebugContext, DebugExplanation


load_dotenv()


class GroqProvider:

    def __init__(self, model: str = "openai/gpt-oss-20b"):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is not set.")

        self.client = Groq(api_key=api_key)
        self.model = model

    def explain_failure(
        self,
        context: DebugContext
    ) -> DebugExplanation:

        prompt = f"""
You are an AI debugging assistant for {context.language}.

Analyze the following failed program execution.

Status:
{context.status}

Code:
```cpp
{context.code}

Input:
{context.input_data}

Expected output:
{context.expected_output}

Actual output:
{context.actual_output}

Compiler/runtime error:
{context.stderr}

Analyze the failure and explain:

1. What went wrong.
2. Why the program produced the observed result.
3. What part of the code is likely responsible.

Do not rewrite the entire program.
Do not invent information that is not supported by the evidence.
Keep the explanation concise and technically accurate.
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "debug_explanation",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "what_went_wrong": {
                                "type": "string"
                            },
                            "why_it_happened": {
                                "type": "string"
                            },
                            "responsible_code": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "what_went_wrong",
                            "why_it_happened",
                            "responsible_code"
                        ],
                        "additionalProperties": False
                    }
                }
            }
        )
        result = response.choices[0].message.content
        data = json.loads(result)

        return DebugExplanation(
            what_went_wrong=data["what_went_wrong"],
            why_it_happened=data["why_it_happened"],
            responsible_code=data["responsible_code"]
        )

