# 🧬 AI-Based Blood Test Report Analyzer

This project uses a multi-agent CrewAI system with Groq LLMs to process and interpret blood test reports. Users upload a PDF report through an API, and the system verifies the document, analyzes medical values, provides nutrition and fitness guidance, and responds intelligently based on the biomarkers detected.

---

## 🛠️ Major Changes — What Changed, Why, and How

Each change below is documented independently with:

- ✅ **What Changed**
- 💡 **Why It Was Changed**
- 🔧 **How It Was Implemented**

---

### 1. ✅ Replaced Comedic Agents with Realistic Medical Agents

💡 **Why**: Agents like “Doctor Who Makes Stuff Up” and “Salesy Nutritionist” were fictional and not suitable for professional or academic use.

🔧 **How**:
- Defined professional roles:
  - `doctor`: Clinical interpretation of lab values.
  - `verifier`: Checks if the uploaded document is a valid blood report.
  - `nutritionist`: Detects nutritional deficiencies.
  - `exercise_specialist`: Recommends exercise plans based on blood markers.
- Removed fictional backstories and unrealistic goals.
- Used `allow_delegation` based on specialization needs.

---

### 2. ✅ Implemented `BloodTestReportTool` Using `PyPDFLoader`

💡 **Why**: The previous tool was a placeholder with no real PDF parsing ability.

🔧 **How**:
- Used `langchain_community.document_loaders.PyPDFLoader` to load PDF pages.
- Cleaned text using `.replace()`, `.strip()`, and whitespace handling.
- Returned concatenated text of all readable pages.

---

### 3. ✅ Added PDF Validation & File Existence Checks

💡 **Why**: Without checks, uploading a non-PDF or broken path would crash the app.

🔧 **How**:
- Checked:
  - If file exists (`os.path.exists`)
  - If path ends in `.pdf`
- Returned error messages if invalid.

---

### 4. ✅ Added Token Limit Truncation

💡 **Why**: Large PDFs could overflow token limits in the LLM input.

🔧 **How**:
- Set a `max_chars = 2000` limit in `BloodTestReportTool`.
- Truncated long reports and appended a warning note:
  `"Content truncated for processing"`

---

### 5. ✅ Created Functioning `NutritionTool`

💡 **Why**: Previous version was a stub.

🔧 **How**:
- Converted report content to lowercase.
- Used `if "keyword" in data` to detect:
  - Vitamin D
  - B12
  - Iron
  - Calcium
  - Cholesterol
  - Glucose
- Returned medically valid food and supplement advice per marker.

---

### 6. ✅ Created Functioning `ExerciseTool`

💡 **Why**: Like the nutrition tool, it returned placeholder text.

🔧 **How**:
- Detected markers like:
  - "cholesterol"
  - "diabetes"
  - "vitamin d"
  - "anemia"
- Suggested exercise plans based on chronic condition indicators.
- Included general fallback plans if no specific markers matched.

---

### 7. ✅ Rewrote Task Definitions with Realistic Goals

💡 **Why**: Tasks previously encouraged contradiction, fiction, and unsafe medical advice.

🔧 **How**:
- Defined proper `description` and `expected_output` for:
  - `verification`
  - `help_patients`
  - `nutrition_analysis`
  - `exercise_planning`
- Set task `context` chains to ensure output from one agent flows to the next.

---

### 8. ✅ Connected Tasks and Agents with Context Passing

💡 **Why**: Tasks were previously independent and had no dependency chain.

🔧 **How**:
- `help_patients` uses `verification` context.
- `nutrition_analysis` uses output from `help_patients`.
- `exercise_planning` uses both `help_patients` and `nutrition_analysis`.

---

### 9. ✅ Added Secure LLM Initialization with `.env`

💡 **Why**: Model and API keys were previously hardcoded or missing.

🔧 **How**:
- Loaded keys from `.env`:
  - `GROQ_API_KEY`
  - `MODEL` (default: `groq/llama-3.1-8b-instant`)
- Created `llm = LLM(...)` object.
- Injected `llm` into all agents.

---

### 10. ✅ Built a FastAPI App with PDF Upload Support

💡 **Why**: No API existed to test the system with real data.

🔧 **How**:
- Created FastAPI app with `/analyze` endpoint.
- Used `UploadFile` to accept `.pdf` files.
- Stored uploaded file with a unique UUID.
- Called `run_crew(query, file_path)` to launch the Crew.

---

### 11. ✅ Added File Type and Save Validation in API

💡 **Why**: Uploading non-PDFs or broken files previously failed silently.

🔧 **How**:
- Checked `.endswith('.pdf')` in API.
- Verified file exists before running Crew.
- Raised `HTTPException` if checks failed.

---

### 12. ✅ Added Automated File Cleanup

💡 **Why**: Temporary files would otherwise build up.

🔧 **How**:
- Wrapped analysis in a `try/finally` block.
- Used `os.remove(file_path)` to delete uploaded file after processing.

---

### 13. ✅ Enabled Detailed Logging for Debugging

💡 **Why**: No debug info was available for backend errors.

🔧 **How**:
- Added `print()` statements for:
  - File path
  - Query
  - Cleanup status
  - Crew execution errors

---

### 14. ✅ Replaced Hardcoded Text in LLM Calls with User Inputs

💡 **Why**: Old agents and tasks used fixed text (e.g., `{query}` not passed properly).

🔧 **How**:
- Passed `inputs={"query": ..., "file_path": ...}` to `crew.kickoff()`.
- Allowed dynamic responses based on user queries and real blood reports.

---

### 15. ✅ Removed `max_iter` and `max_rpm` Constraints in Agents

💡 **Why**: These limited the model's ability to reason fully.

🔧 **How**:
- Removed `max_iter` and `max_rpm` fields from new agents for more flexible processing.

---

## ✅ System Pipeline Overview

1. 📝 User uploads blood test report (PDF)
2. ✅ `verifier` checks if it's a valid report
3. 🧠 `doctor` analyzes blood markers
4. 🥗 `nutritionist` suggests diet improvements
5. 🏃 `exercise_specialist` gives a workout plan
6. 📤 FastAPI returns structured recommendations

---

## 📦 Submission-Ready Improvements

| Change Area           | Before                      | After                                      |
|------------------------|-----------------------------|---------------------------------------------|
| Agent Logic            | Comedic, fictional          | Clinical, role-specific agents              |
| PDF Handling           | No real reading             | Functional parser + validation + truncation |
| Token Safety           | Not managed                 | 2000-char truncation for LLM input          |
| Nutrition/Exercise     | Not implemented             | Marker-based actionable logic               |
| Tasks                  | Random output               | Structured expectations + chaining          |
| API Interface          | Missing                     | FastAPI with file upload + output JSON      |
| Error Handling         | Weak                        | Robust, detailed exception flow             |
| LLM Connection         | Mocked or broken            | `.env` driven Groq LLM setup                |

---

## 📎 Future Recommendations

- Add PDF summary download (text → PDF)
- Store processed reports and agent logs
- Add frontend for form-based interaction
- Extend support to lab reports beyond blood (e.g., urine, imaging)

