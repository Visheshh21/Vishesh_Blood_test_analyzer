## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()
from litellm import completion

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from tools import search_tool, blood_test_tool

### Loading LLM
import os
llm = LLM(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("MODEL","groq/llama-3.1-8b-instant"),
)
print("✅ GROQ_API_KEY is:", os.getenv("GROQ_API_KEY"))  # Debug: Should print actual key (partially masked)

# Creating an Experienced Doctor agent
doctor = Agent(
    role="Senior Medical Doctor and Blood Test Specialist",
    goal=(
        "Carefully review and interpret the patient's blood test results. "
        "Identify any abnormal values, explain their clinical relevance, and provide a clear summary of possible medical implications. "
        "Use the blood test tool to read the report data first."
    ),
    verbose=True,  # Enable for debugging
    memory=False,
    backstory=(
        "You are a senior medical doctor with over 15 years of experience in clinical pathology. "
        "You specialize in analyzing blood test reports, diagnosing underlying conditions, and explaining findings in a clear and actionable manner."
    ),
    tools=[blood_test_tool],
    llm=llm,
    # Removed max_iter and max_rpm restrictions
    allow_delegation=False
)

verifier = Agent(
    role="Medical Document Validator",
    goal=(
        "Validate the uploaded document to ensure it is a legitimate blood test report. "
        "Use the blood test tool to read and verify the document structure and content."
    ),
    verbose=True,
    memory=False,
    backstory=(
        "You are a medical documentation expert trained in validating laboratory reports. "
        "You ensure the data integrity of clinical records before they are used for diagnosis or treatment planning."
    ),
    tools=[blood_test_tool],
    llm=llm,
    allow_delegation=False
)

nutritionist = Agent(
    role="Clinical Nutritionist and Dietitian",
    goal=(
        "Based on the verified blood test data, identify nutritional deficiencies or imbalances. "
        "Offer evidence-based dietary recommendations tailored to the patient's biomarkers."
    ),
    verbose=True,
    memory=False,
    backstory=(
        "You are a licensed dietitian specializing in interpreting lab results to create personalized nutrition plans. "
        "You focus on optimizing health outcomes through diet and nutritional therapy informed by clinical data."
    ),
    llm=llm,
    allow_delegation=False
)

exercise_specialist = Agent(
    role="Clinical Exercise Physiologist",
    goal=(
        "Based on the blood test findings, assess the patient's health status and recommend a safe, personalized exercise plan. "
        "Account for indicators of cardiovascular, metabolic, and musculoskeletal health."
    ),
    verbose=True,
    memory=False,
    backstory=(
        "You are a certified exercise physiologist with expertise in prescribing exercise for individuals with chronic conditions. "
        "You integrate blood test data with physical activity guidelines to create customized fitness plans."
    ),
    llm=llm,
    allow_delegation=False
)
