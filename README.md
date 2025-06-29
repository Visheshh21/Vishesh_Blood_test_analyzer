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

### 11. ✅ Removed `max_iter` and `max_rpm` Constraints in Agents

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
## ⚡ Quick Setup
### ✅ Prerequisites

```bash
Python 3.9+
Groq API key
UV installer (recommended)
```
### 🔧 Installation with UV
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv tool install crewai
```
### 📂 Clone repository
```bash
🌐 git clone https://github.com/your-username/blood-test-analyzer.git
cd blood-test-analyzer
```
### Create and activate virtual environment (recommended)
```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
### 📦 Install dependencies
pip install -r requirements.txt
### 🔐 Create .env file:
Edit .env with your credentials:
```bash
GROQ_API_KEY=your_api_key_here
MODEL=groq/llama3-70b-8192  # Recommended model
```
### 🏃 Running the Application
- 🛠️ Development Mode
```bash
uvicorn main:app --reload
```
- 🚢 Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
---
## 📡 API Documentation

### 📍 Base URL
```
http://localhost:8000
```

--

### 🚀 GET /
Performs a health check.
```json
{
  "message": "Blood Test Report Analyser API is running"
}
```

--

### 🧾 POST /analyze
Uploads a blood test report (PDF) and returns detailed AI-driven analysis.

**Content-Type:** `multipart/form-data`

#### 📥 Form Fields

| Field   | Type     | Required | Description                   |
|---------|----------|----------|-------------------------------|
| file    | PDF file | ✅       | The PDF blood report          |
| query   | string   | ❌       | Custom query (optional input) |

--

#### 💡 Example
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@blood_report.pdf" \
  -F "query=Summarize my blood test"
```

--

#### 📤 Response
```json
{
  "status": "success",
  "query": "Summarize my blood test",
  "analysis": "[Results from agents]",
  "file_processed": "blood_report.pdf"
}
```
---
## 🤖 Agents Overview

### 🧑‍⚕️ Doctor Agent
**Role:** Senior Medical Doctor and Blood Test Specialist  
**Purpose:** Provides clinical interpretation of blood test results with medical accuracy  
**Tools:** `blood_test_tool` for PDF parsing and analysis 

### 🔍 Verifier Agent
**Role:** Medical Document Verification  
**Purpose:** Validates uploaded documents to ensure they are legitimate blood test reports  
**Tools:** `blood_test_tool` for document structure validation

### 🥗 Nutritionist Agent
**Role:** Clinical Nutritionist and Dietitian  
**Purpose:** Identifies nutritional deficiencies and provides evidence-based dietary recommendations  
**Tools:** Uses context from previous agents (no direct tools)

### 🏋️ Exercise Specialist Agent
**Role:** Clinical Exercise Physiologist  
**Purpose:** Recommends safe, personalized exercise plans based on blood test findings
**Tools:** Uses health context from Doctor and Nutritionist agents

### 📋 Workflow
- Verification → Document validation and structure check
- Medical Analysis → Clinical interpretation of biomarkers
- Nutritional Assessment → Diet recommendations based on deficiencies
- Exercise Planning → Safe fitness recommendations aligned with health status

## 🧪 Testing

You can test the API using **Postman**:

### Endpoint
**Method:** `POST`  
**URL:** `http://localhost:8000/analyze`

### Body (form-data)
| Key   | Type | Description                     |
|-------|------|---------------------------------|
| file  | File | Upload the PDF file to analyze |
| query | Text | Enter your question or prompt  |

Make sure to set the **Body type to `form-data`** in Postman and correctly upload your file along with the query.

### Sample Output
![WhatsApp Image 2025-06-29 at 02 35 15_c075e1d7](https://github.com/user-attachments/assets/2d91acf9-0909-411f-9438-210b9080c6ad)
