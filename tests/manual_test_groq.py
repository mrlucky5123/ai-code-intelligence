from engine.ai.models import DebugContext
from engine.ai.groq_provider import GroqProvider


context = DebugContext(
    code="""
#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;

    cout << a - b;
}
""",
    language="cpp",
    input_data="5 3",
    expected_output="8",
    actual_output="2",
    status="wrong_answer",
    stderr=""
)


provider = GroqProvider()

result = provider.explain_failure(context)

print("\n===== AI DEBUG EXPLANATION =====\n")
print("What went wrong:")
print(result.what_went_wrong)

print("\nWhy it happened:")
print(result.why_it_happened)

print("\nResponsible code:")
print(result.responsible_code)