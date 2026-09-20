const codeInput = document.getElementById("code");
const inputField = document.getElementById("input");
const expectedOutputField = document.getElementById("expected-output");

const analyzeButton = document.getElementById("analyze-button");

const resultSection = document.getElementById("result-section");
const statusElement = document.getElementById("status");

const expectedResult = document.getElementById("expected-result");
const actualResult = document.getElementById("actual-result");

const aiSection = document.getElementById("ai-section");
const explanationElement = document.getElementById("explanation");


analyzeButton.addEventListener("click", analyzeCode);


async function analyzeCode() {

    const code = codeInput.value.trim();
    const input = inputField.value;
    const expectedOutput = expectedOutputField.value.trim();

    if (!code) {
        alert("Please enter your C++ code.");
        return;
    }

    if (!expectedOutput) {
        alert("Please enter the expected output.");
        return;
    }

    analyzeButton.disabled = true;
    analyzeButton.textContent = "Analyzing...";

    resultSection.classList.add("hidden");
    aiSection.classList.add("hidden");

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/v1/analyze",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    code: code,
                    language: "cpp",
                    input: input,
                    expected_output: expectedOutput
                })
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "Something went wrong."
            );
        }

        showResult(result);

    } catch (error) {

        alert("Could not connect to the backend.");

        console.error(error);

    } finally {

        analyzeButton.disabled = false;
        analyzeButton.textContent = "Analyze Code";
    }
}


function showResult(result) {

    resultSection.classList.remove("hidden");

    statusElement.textContent =
        result.status.replace("_", " ").toUpperCase();

    expectedResult.textContent =
        result.expected_output || "";

    actualResult.textContent =
        result.actual_output || "";

    if (result.explanation) {

        aiSection.classList.remove("hidden");

        explanationElement.textContent =
            result.explanation;
    }
}