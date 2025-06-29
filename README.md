# 🧬 AI-Based Blood Test Report Analyzer Assignment (Vishesh Goel)

This project uses a multi-agent system powered by CrewAI and Groq LLMs to analyze blood test reports. It reads PDF files, verifies report validity, interprets biomarkers, and delivers medical, nutritional, and fitness recommendations through a FastAPI interface. It simulates realistic health consultation using AI tools.

---

## 🔧 Major Codebase Changes – Documented

Below are all the major changes made across the codebase, along with:

- ✅ **What Changed**
- 💡 **Why It Was Changed**
- 🔧 **How It Was Implemented**

---

### 1. 🧑‍⚕️ Agent Role Rewriting

✅ **What Changed**  
Old agents were humorous, illogical characters (e.g., “Doctor Who Makes Stuff Up”, “Salesy Nutritionist”).

💡 **Why Changed**  
To ensure professionalism, clinical realism, and appropriate behavior from the LLMs during blood report interpretation.

🔧 **How Changed**  
Replaced all agents with real-world equivalents:
- `doctor`: Senior Medical Doctor
- `verifier`: Medical Document Validator
- `nutritionist`: Clinical Nutritionist
- `exercise_specialist`: Certified Exercise Physiologist

Each agent has a detailed backstory, clear goals, and delegation control.

---

### 2. 🛠️ Tooling Overhaul – PDF, Nutrition & Exercise Tools

✅ **What Changed**  
- Old `BloodTestReportTool`, `NutritionTool`, and `ExerciseTool` were placeholders or non-functional stubs.
  
💡 **Why Changed**  
They were either empty, returned hardcoded strings, or not used in the crew pipeline.

🔧 **How Changed**  
- Introduced a working `BloodTestReportTool` using `PyPDFLoader` from LangChain.
- Added:
  - File validation
  - Truncated output for long reports
  - Whitespace and format cleanup
- Implemented keyword-based logic in `NutritionTool` and `ExerciseTool` to give recommendations based on actual medical markers.

---

### 3. 📋 Task Redesign – Meaningful Instructions & Outputs

✅ **What Changed**  
Previous tasks had vague or satirical descriptions (e.g., "Make up scary diagnoses", "Just say it's a blood report").

💡 **Why Changed**  
To provide clear task delegation and ensure multi-agent collaboration for real-world use cases.

🔧 **How Changed**  
- All `Task` objects now have:
  - Domain-relevant `description`
  - Clear `expected_output` format
  - Logical `context` dependencies (e.g., nutrition follows doctor's output)
- Tasks added:
  - `verification` → checks report validity
  - `help_patients` → main analysis
  - `nutrition_analysis` → diet suggestions
  - `exercise_planning` → fitness advice

---

### 4. 🌐 FastAPI Integration & Uploader Logic

✅ **What Changed**  
The previous code had no working API or file input/output. It was a simple script with hardcoded paths.

💡 **Why Changed**  
A web API was needed to upload PDFs and get responses dynamically from agents.

🔧 **How Changed**  
- Introduced FastAPI-based backend in `main.py`
- Added `/analyze` endpoint to:
  - Accept PDF file and custom query
  - Save file to `/data` directory
  - Pass `query` and `file_path` to the Crew
  - Return structured JSON output
- Includes error handling, file type checks, and post-processing cleanup.

---

### 5. 🔐 LLM Initialization & Environment Config

✅ **What Changed**  
LLMs were either mocked or improperly initialized with hardcoded values.

💡 **Why Changed**  
Needed real model access using Groq and secure key management.

🔧 **How Changed**  
- Introduced `.env` for managing:
  - `GROQ_API_KEY`
  - `MODEL` (default to `groq/llama-3.1-8b-instant`)
- Added a proper `LLM` object initialization using `os.getenv`
- Connected this LLM instance to all agents via their `llm` parameter

---

### 6. 🧪 Improved Error Handling & Debug Logging

✅ **What Changed**  
Original code had no input validation, no exception handling, and no logging.

💡 **Why Changed**  
To avoid silent failures and make the app robust and traceable.

🔧 **How Changed**  
- All tools and FastAPI routes now use `try/except` blocks
- Verbose logging added in:
  - `run_crew()` function
  - Agent configurations
  - File I/O logic
- Fails gracefully if:
  - File isn't a PDF
  - File is unreadable
  - Crew fails to execute

---

## ✅ Summary of Enhancements

| Area                | Before                              | After                                    |
|---------------------|--------------------------------------|-------------------------------------------|
| Agent Design         | Comedic and illogical                | Clinical and domain-specific              |
| PDF Reader Tool      | Non-functional async placeholder     | Real parser with validation and formatting|
| Nutrition & Exercise | Not implemented                     | Keyword-based, medically informed logic   |
| API Layer            | Missing                             | FastAPI with file upload & result return  |
| LLM Connection       | Hardcoded / mocked                  | `.env`-driven, Groq-powered initialization|
| Task Design          | Random text generators              | Chainable, descriptive, output-focused    |

---

## 🏁 Project Outcome

After applying the above changes, the system is now a modular, testable, and realistic blood test analyzer capable of being used in a real-world AI health assistant setting.

